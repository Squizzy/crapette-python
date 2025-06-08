from constants import Players
from network_messages import ServerNetworkMessage
from json import loads

from icecream import ic # type: ignore
ic.configureOutput(prefix="message_decoder: ")
def log_message(message: str):
    DEBUG = True
    if DEBUG:
        ic(message)


def decode_player_id(message: str) -> Players:
    log_message("decoding player_id")
    msg = loads(message)
    log_message(msg)
    if msg["type"] == ServerNetworkMessage.SENDING_PLAYER_ID.value:
        if msg["target"] == "":
            return Players[msg["value"]]

    else:
        raise ValueError("Incorrect message, no player ID included, or the message was not intended for this player")
    
    return Players.ERROR