# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
import bot_runner
from search.searchers.inverseIndexSearcher import InverseIndexSearcher

if __name__ == '__main__':
    try:
        bot_runner.run()
    except Exception as e:
        print("exit")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
