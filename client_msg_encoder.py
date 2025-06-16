from json import dumps
from abc import ABC, abstractmethod

from network_messages import ClientNetworkMessage

from game_logger import GameLogger, DebugLevel
client_logger: GameLogger = GameLogger("client_msg_eencoder", level=DebugLevel.client_msg_encoder.value)


class ClientMessageEncoderInterface(ABC):
    @abstractmethod
    def encode_request(self, message: ClientNetworkMessage) -> str:
        """Encode a request message to be sent to the server"""
        pass
        
        
class ClientMessageEncoder(ClientMessageEncoderInterface):
    def __init__(self):
        ...
        
    def encode_request(self, message: ClientNetworkMessage) -> str:
        msg = {
            "type": message.value,
            "target": "",
            "value": "",
            }
        return dumps(msg)

