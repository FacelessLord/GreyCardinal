import os.path
import json
import re
from collections import defaultdict
from typing import List, Dict

from search.collections.customizedHashSet import CustomizedHashSet
from search.searchers.baseSearcher import BaseSearcher
from search.typings import SearchResult, SearchObject


def load_json(path):
    json_path = os.path.join(os.getcwd(), path)
    if not os.path.exists(json_path):
        return {}
    with open(json_path, "r") as f:
        lines = f.readlines()
    return json.JSONDecoder().decode(str.join("", lines))


def serialize_data(data: SearchObject) -> str:
    if data.type != 'text':
        raise ValueError()
    return data.data


def deserialize_data(type: str, data):
    if type == 'text':
        return SearchObject(type, data)
    raise ValueError(type)


class InverseIndexSearcher(BaseSearcher):
    def __init__(self, store_path: str):
        super().__init__()
        self.store_path = store_path
        self.index: Dict[Dict] = None
        self.data_keys = {"max": 0}
        self.accepted_data: List[SearchObject] = []
        self.temporal_index_prep: Dict[int, List[(str, int)]] = {}
        self.temporal_index = defaultdict(dict)

    # Loads index and possibly data from drive
    def load(self):
        self.load_keys()
        self.load_index()

    def load_keys(self):
        self.data_keys = load_json(self.store_path + "_keys.json")

    def load_index(self):
        self.index = load_json(self.store_path + "_index.json")

    # Uses it's index to find most relevant data to match the query
    def find(self, query: str) -> SearchResult:
        words = self.extract_words(query)
        sets = list(map(lambda w: self.index[w], filter(lambda w: w in self.index, words))) if self.index is not None else []
        temporal_sets = list(map(lambda w: self.temporal_index[w], filter(lambda w: w in self.temporal_index, words))) if self.temporal_index is not None else []
        if len(sets) == 0 and len(temporal_sets) == 0:
            return SearchResult(True, [])

        sets.extend(temporal_sets)
        result = CustomizedHashSet(lambda x: x[0], sets[0].items())

        for s in sets:
            result.intersection_update(s.items())

        result = list(map(lambda x: x[0], result))

        ranging = defaultdict(lambda: 0)
        for d in result:
            for w in words:
                if self.index is not None and w in self.index and d in self.index[w]:
                    ranging[d] += self.index[w][d]
                if self.temporal_index is not None and w in self.temporal_index and d in self.temporal_index[w]:
                    ranging[d] += self.temporal_index[w][d]

        ranged_result = sorted(result, key=lambda d: ranging[d], reverse=True)

        for doc in ranged_result:
            data = self.get(doc)
            print(data.data)

        return SearchResult(True, ranged_result)

    # Accepts new data to store and extends it's index
    def accept(self, data: SearchObject):
        if data.type != "text":
            raise ValueError(f"{data.type} is not supported by IIS")
        self.update_temporal_index(data, self.data_keys["max"] + len(self.accepted_data))
        self.accepted_data.append(data)

    wordRe = re.compile(r"[\w\dа-яА-ЯёЁ]+")

    def extract_words(self, text: str):
        return self.wordRe.findall(text)

    def update_temporal_index(self, data: SearchObject, pos: int):
        if data.type != "text":
            return
        words = self.extract_words(data.data)
        words_dict: defaultdict[str, int] = defaultdict(lambda: 0)
        for w in words:
            words_dict[w] += 1
        pairs = []
        for p in words_dict.items():
            pairs.append(p)
            self.temporal_index[p[0]][pos] = p[1]
        self.temporal_index_prep[pos] = pairs

    # Accesses data by it's key
    def get(self, key) -> SearchObject:
        max_saved_key = self.data_keys["max"]
        if key >= max_saved_key:
            accepted_key = key - max_saved_key
            if len(self.accepted_data) <= accepted_key:
                return SearchObject("None", "Ничего не нашлось")
            return self.accepted_data[accepted_key]

        if key not in self.data_keys:
            return SearchObject("None", "Поиск сломался")
        (offset, type, length) = self.data_keys[key]
        with open(self.store_path + "_data", "r") as f:
            f.seek(offset)
            serialized_data = f.read(length)
        data = deserialize_data(type, serialized_data)
        return data

    # Unloads index and accepted data to the drive
    def store(self):
        self.store_data()
        self.store_keys()
        self.store_index()

        self.accepted_data.clear()

    def store_index(self):
        self.imprint_index()

        index_path = os.path.join(os.getcwd(), self.store_path + "_index.json")
        lines = json.JSONEncoder().encode(self.index)
        with open(index_path, "w") as f:
            f.writelines(lines)

    def imprint_index(self):
        for i, d in enumerate(self.accepted_data):
            key: (int, str, int) = d.data_key
            prepared_data: List[(str, int)] = self.temporal_index_prep[i]
            for word, count in prepared_data:
                if word not in self.index:
                    self.index[word] = []
                self.index[word][key[3]] = count

        self.temporal_index_prep.clear()
        self.temporal_index.clear()

    def store_data(self):
        data_path = os.path.join(os.getcwd(), self.store_path + "_data")
        f = open(data_path, "a")

        for data in self.accepted_data:
            offset = f.tell()
            serializedData = serialize_data(data)
            key = (offset, data.type, len(serializedData), self.data_keys["max"])
            data.data_key = key
            self.data_keys[self.data_keys["max"]] = key
            self.data_keys["max"] += 1
            f.write(serializedData)

        f.flush()
        f.close()

    def store_keys(self):
        key_path = os.path.join(os.getcwd(), self.store_path + "_keys.json")
        lines = json.JSONEncoder().encode(self.data_keys)
        with open(key_path, "w") as f:
            f.writelines(lines)

    def clean(self):
        self.index and self.index.clear()
        self.temporal_index.clear()
        self.temporal_index_prep.clear()
        self.accepted_data.clear()
        self.data_keys = {"max": 0}

        data_path = os.path.join(os.getcwd(), self.store_path + "_data")
        open(data_path, 'w').close()

        self.store()
