from search.searchers.inverseIndexSearcher import InverseIndexSearcher
from search.typings import SearchObject

if __name__ == '__main__':
    searcher = InverseIndexSearcher("data\\iis")

    data1 = SearchObject("text", "Priovacalanta di, niotymo sakvigani; la 53")
    data2 = SearchObject("text", "Пока, буквы можешь оставить себе")
    data3 = SearchObject("text", "Привет, вот тебе буквы:")

    searcher.load()
    searcher.accept(data1)
    searcher.accept(data3)
    searcher.accept(data2)

    res = searcher.find("буквы")
    print(res.items)

