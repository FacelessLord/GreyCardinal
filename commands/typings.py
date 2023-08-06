from typing import Literal


class CommandResult:
    # finish | default | <commandName>
    def __init__(self, next_state, data=None):
        self.next_state = next_state
        self.data = data

    @staticmethod
    def default():
        return CommandResult("default")

    @staticmethod
    def state(new_state: str):
        return CommandResult(new_state)

    @staticmethod
    def finish():
        return CommandResult("finish")
