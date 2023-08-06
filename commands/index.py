import telepot.aio

from bot.typings import GreyContext
from commands.base import Command
from commands.typings import CommandResult
from search.searchers.inverseIndexSearcher import InverseIndexSearcher
from search.typings import SearchObject


class IndexCommand(Command):
    def __init__(self):
        super().__init__("index")
        self.searcher = InverseIndexSearcher("data\\iis")

    async def on_start(self, bot: telepot.aio.Bot, ctx: GreyContext, text: str, msg) -> CommandResult:
        operation = text.split(" ")[0].strip()
        query = text[len(operation):].strip()
        if operation == 'load':
            self.searcher.load()
        elif operation == "store":
            self.searcher.store()
        elif operation == "find":
            result = self.searcher.find(query)
            await bot.sendMessage(ctx.chat_id, f"Нашла {len(result.items)} результатов")
        elif operation == "accept":
            obj = SearchObject("text", query)
            self.searcher.accept(obj)
        elif operation == "get":
            data = self.searcher.get(query)
            await bot.sendMessage(ctx.chat_id, data.data)
        elif operation == "clean":
            self.searcher.clean()
        else:
            await bot.sendMessage(ctx.chat_id, "Не понимаю")

        return CommandResult.finish()

