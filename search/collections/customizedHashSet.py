from typing import List, Any


class CustomizedHashSet:
    def __init__(self, key_selector, iterable=None):
        self._count = 0
        self._key_selector = key_selector
        self._buckets_size = 11
        self._items = list([None] * self._buckets_size)

        if iterable is not None:
            for item in iterable:
                self.add(item)

    def add(self, item):
        key = self._key_selector(item)
        ind = hash(key) % len(self._items)

        chain = self._items[ind]
        while chain is not None:
            if self._key_selector(chain[0]) == key:
                return
            chain = chain[1]

        self._items[ind] = (item, self._items[ind])
        self._count += 1

        # TODO check and rebuild

    def __contains__(self, item) -> bool:
        key = self._key_selector(item)
        ind = hash(key) % len(self._items)

        chain = self._items[ind]
        while chain is not None:
            if self._key_selector(chain[0]) == key:
                return True
            chain = chain[1]

        return False

    def remove(self, item) -> bool:
        key = self._key_selector(item)
        ind = hash(key) % len(self._items)

        chain: List[Any] = self._items[ind]

        if chain is None:
            return False

        if self._key_selector(chain[0]) == key:
            self._items[ind] = chain[1]
            self._count -= 1
            return True

        while chain[1] is not None:
            if self._key_selector(chain[1][0]) == key:
                chain[1] = chain[1][1]
                self._count -= 1
                return True
            chain = chain[1]

        return False

    def intersection_update(self, iterable):
        for item in iterable:
            self.add(item)

    def __len__(self):
        return self._count

    def __iter__(self):
        return CustomizedHashSetIterator(self._items)


class CustomizedHashSetIterator:
    def __init__(self, src_items):
        self.src_items = src_items
        self.bucket_index = -1
        self.chain_item = None

    def __next__(self):
        while self.chain_item is None:
            self.bucket_index += 1
            if self.bucket_index >= len(self.src_items):
                raise StopIteration()
            self.chain_item = self.src_items[self.bucket_index]

        item = self.chain_item[0]
        self.chain_item = self.chain_item[1]
        return item
