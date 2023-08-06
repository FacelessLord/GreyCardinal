import asyncio

import telepot
from telepot.aio.loop import MessageLoop

from commands.index import IndexCommand
from commands.typings import CommandResult
from commands.base import Command
from commands.mock import MockCommand
from bot.typings import GreyContext


class GreyBot:
    def __init__(self, token):
        self.bot = telepot.aio.Bot(token)
        self.currentCommand: Command = None
        self.commands = {
            "mock": MockCommand(),
            "index": IndexCommand(),
        }
        self.defaultHandler: Command = None
        self.data = None

    def start(self):
        bot_loop = MessageLoop(self.bot, self.handle)

        print('Listening ...')
        loop = asyncio.get_event_loop()
        loop.create_task(bot_loop.run_forever())
        loop.run_forever()

    async def handle(self, msg):
        result = None
        content_type, chat_type, chat_id = telepot.glance(msg)
        ctx = GreyContext(chat_id, chat_type, content_type)
        try:
            if not self.currentCommand:
                if content_type != 'text':
                    await self.bot.sendMessage(chat_id, "Go fuck")
                    return
                text: str = msg["text"]
                if not text.startswith("/"):
                    await self.bot.sendMessage(chat_id, "Go fuck")
                    return

                command = text[1:].split(" ")[0]
                if command in self.commands:
                    print("Command: " + command)
                    command_processor: Command = self.commands[command]
                    result = await command_processor.on_start(self.bot, ctx, text[1 + len(command):].strip(), msg)
                    self.handle_result(command_processor, result)
                elif self.defaultHandler:
                    print("Default")
                    result = await self.defaultHandler.on_start(self.bot, ctx, text[1 + len(command):].strip(), msg)
                    self.handle_result(self.defaultHandler, result)
            else:
                print("CC: " + self.currentCommand.name)
                result = await self.currentCommand.on_next(self.bot, ctx, msg, self.data)
                self.handle_result(self.currentCommand, result)
        except Exception as e:
            print(e)
            await self.bot.sendMessage(chat_id, "Error")
            self.currentCommand = None

    def handle_result(self, command, result: CommandResult):
        if result.next_state == 'finish':
            self.currentCommand = None
        elif result.next_state == 'default':
            self.currentCommand = command
        elif result.next_state in self.commands:
            self.currentCommand = self.commands[result.next_state]
        else:
            raise ValueError(result.next_state)
