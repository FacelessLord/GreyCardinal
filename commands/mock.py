import telepot.aio

from commands.typings import CommandResult
from commands.base import Command
from bot.typings import GreyContext


class MockCommand(Command):
    def __init__(self):
        super().__init__("mock")

    async def on_start(self, bot: telepot.aio.Bot, ctx: GreyContext, text: str, msg) -> CommandResult:
        await bot.sendMessage(ctx.chat_id, text)
        return CommandResult("default")
