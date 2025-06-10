from constants import Players
from network_messages import ServerNetworkMessage, ClientNetworkMessage
from json import dumps

from icecream import ic # type: ignore
ic.configureOutput(prefix="message_encoder: ")
def log_message(message: str):
    DEBUG = True
    if DEBUG:
        ic(message)
        

def encode_request(message: ClientNetworkMessage) -> str:
    msg = {
        "type": message.value,
        "target": "",
        "value": "",
        }
    
    return dumps(msg)



def encode_player_id(player: Players) -> str:
    
    log_message("encoding player_id")
    msg = {
        "type": ServerNetworkMessage.SENDING_PLAYER_ID.value,
        #TODO: Implement a message target
        "target": "",
        "value": player.name,
        }
    log_message(f"{msg}")
    
    return dumps(msg)

def encode_stacks_cards(stacks_cards: dict[str, list[str]]) -> str:
    log_message("encoding stacks_cards")
    msg = {
        "type": ServerNetworkMessage.SENDING_STACKS_CARDS.value,
        "target": "",
        "value": stacks_cards,
        }
    log_message(f"{msg}")

    return dumps(msg)