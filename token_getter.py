import re

from errors.TokenNotFoundError import TokenNotFoundError


def get_token(verbose: bool = False):
    token = read_token()
    if not token:
        if verbose:
            print("Can't find bot token, enter one, please:")
            counter = 3
            while not token and counter > 0:
                token = input()
                if not re.match("\\d+:\\w+-\\w+", token):
                    if counter > 1:
                        print("Doesn't look like correct token. Enter correct one:")
                    token = None
                    counter -= 1
            else:
                if counter == 0:
                    raise TokenNotFoundError()
                print("Token will be saved in token.txt")

            print("Success!")
            save_token(token)
        else:
            raise TokenNotFoundError()
    return token


def read_token():
    # os.path.exists(path)
    token = None
    with open("token.txt", "r") as tokenFile:
        token = tokenFile.readline()
    return token and token.strip()


def save_token(token):
    with open("token.txt", "w") as tokenFile:
        tokenFile.write(token)
        tokenFile.flush()
