from typing import List


class SearchObject:
    # type = text | None
    def __init__(self, type: str, data):
        self.type = type
        self.data = data
        self.data_key: (int, str, int) = None


class SearchItem(SearchObject):
    # type = text | None
    def __init__(self, type: str, data, relevancy: float):
        super().__init__(type, data)
        self.relevancy = relevancy


class SearchResult:
    def __init__(self, is_success: bool, items: List[SearchItem]):
        self.is_success = is_success
        self.items = items
