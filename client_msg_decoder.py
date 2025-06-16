from json import loads
from abc import ABC, abstractmethod

from constants import Players

from game_logger import GameLogger, DebugLevel
client_logger: GameLogger = GameLogger("client_msg_decoder", level=DebugLevel.client_msg_decoder.value)


class ClientMessageDecoderInterface(ABC):
    @abstractmethod
    def decode_player_id(self, message: str) -> Players:
        """Decode the player id from the received message"""
        pass
    
    @abstractmethod
    def decode_stacks_cards(self, message: str) -> dict[str, dict[str, list[str]]]:
        """Decode the stacks cards from the received message"""
        pass


class ClientMessageDecoder(ClientMessageDecoderInterface):

    def __init__(self):
        ...

    def decode_player_id(self, message: str) -> Players:
        
        client_logger.info("decoding player_id")
        
        received_value = loads(message)["value"]

        try:
            player = Players[str(received_value)]
        except KeyError as e:
            client_logger.error(f"received player_id is not a valid player id: {e}")
            return Players.ERROR
        
        client_logger.debug(f"{player=}")
        
        return player
        
        # client_logger.info("decoding player_id")
        # msg = loads(message)
        # client_logger.debug(f"decoded message: {msg}")
        # if msg["type"] == ServerNetworkMessage.SENDING_PLAYER_ID.value:
        #     if msg["target"] == "":
        #         return Players[msg["value"]]

        # else:
        #     raise ValueError("Incorrect message, no player ID included, or the message was not intended for this player")
        
        # return Players.ERROR

    def decode_stacks_cards(self, message: str) -> dict[str, dict[str, list[str]]]:
        
        # Extract the stacks cards from the received message
        received_value = loads(message)["value"]

        # check that data was received, if not it is a problem
        if len(received_value) > 0:
            stacks_cards = received_value
        else:
            client_logger.error("received stacks cards is empty")
            return {}
        
        client_logger.debug(f"retrieved stacks cards: {stacks_cards}")
        
        return stacks_cards
        
        # received_message = loads(message)
        
        # if received_message["type"] == ServerNetworkMessage.SENDING_STACKS_CARDS.value:
        #     stacks = received_message["value"]
        # else:
        #     client_logger.warning("decode_stacks_cards: problem getting the data")
            
        # client_logger.info(f"Cards received: {stacks=}")
        # return {}