from enum import Enum
from stack_crapette import CrapetteStack
from deck import Deck
from constants import Players
from json import dumps, loads

from icecream import ic # type: ignore
ic.configureOutput(prefix="network messages: ")
def log_message(message: str):
    # enable debug messages
    DEBUG = True
    if DEBUG:
        ic(message)




class ClientNetworkMessage(Enum):
    # connectivity messages
    CONNECT  = 'connect'
    DISCONNECT = 'disconnect'
    QUIT = 'quit'
    
    # game messages
    SEND_PLAYER_ID = 'send_player_id'
    SEND_STACKS_CARDS = 'send_stacks_cards'


class ServerNetworkMessage(Enum):
    # connectivity messages

    # game messages
    SENDING_PLAYER_ID = 'sending_player_id'
    SEND_STACKS_CARDS = 'sending_stacks_cards'

class server_message_encoder:
    def player_id(self, player: Players) -> str:
        
        log_message("encoding player_id")
        msg = {
            "type": ServerNetworkMessage.SENDING_PLAYER_ID.value,
            #TODO: Implement a message target
            "target": "",
            "value": player.name,
            }
        log_message(f"{msg}")
        # log_message(player.value)
        # log_message(player.name)
        
        return dumps(msg)
        
    
    
class client_message_decoder:
    def player_id(message: str) -> Players:
        log_message("decoding player_id")
        msg = loads(message)
        log_message(msg)
        if msg["type"] == ServerNetworkMessage.SENDING_PLAYER_ID.value:
            if msg["target"] == "":
                return Players[msg["value"]]

        else:
            raise ValueError("Incorrect message, no player ID included, or the message was not intended for this player")
    
    
    
    def crapette_stack(message: str)  -> CrapetteStack:
        """
        find out in a string received from the server where the crapette stack info is
        Returns:
            The CrapetteStack content
        """
        deck: Deck = Deck()
        deck.shuffle()
        
        temp_crapette_stack = CrapetteStack()
        
        print(message)
        
        return temp_crapette_stack