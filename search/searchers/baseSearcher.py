from search.typings import SearchResult


class BaseSearcher:
    def __init__(self):
        pass

    # Loads index and possibly data from drive
    def load(self):
        raise NotImplementedError()

    # Uses it's index to find most relevant data to match the query
    def find(self, query: str) -> SearchResult:
        raise NotImplementedError()

    # Accepts new data to store and extends it's index
    def accept(self, data):
        raise NotImplementedError()

    # Accesses data by it's key
    def get(self, key):
        raise NotImplementedError()

    # Unloads index and accepted data to the drive
    def store(self):
        raise NotImplementedError()


