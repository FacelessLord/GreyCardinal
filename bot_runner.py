import token_getter
from bot.GreyBot import GreyBot


def run():
    token = token_getter.get_token(True)
    grey_bot = GreyBot(token)
    grey_bot.start()
