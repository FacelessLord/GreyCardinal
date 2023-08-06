import telepot.aio

from commands.typings import CommandResult
from bot.typings import GreyContext


class Command:
    def __init__(self, name):
        self.name = name

    async def on_start(self, bot: telepot.aio.Bot, ctx: GreyContext, text: str, msg) -> CommandResult:
        raise NotImplementedError()

    async def on_next(self, bot: telepot.aio.Bot, ctx: GreyContext, msg, data) -> CommandResult:
        raise NotImplementedError()
