from abc import ABC, abstractmethod
from json import loads

from constants import Players
from client_network import ClientInterface
from network_messages import ClientNetworkMessage, ServerNetworkMessage
# from message_encoder import encode_request
from client_msg_encoder import ClientMessageEncoder
from game_logger import GameLogger

client_logger: GameLogger
# from icecream import ic # type: ignore
# ic.configureOutput(prefix="client_network: ")
# def log_message(message: str):
#     # enable debug messages
#     DEBUG = True
#     if DEBUG:
#         ic(message)
        

class ClientGameCommsInterface(ABC):
    @abstractmethod
    def get_player_id(self)  -> Players:
        """Request the player ID from the server"""
        pass

    @abstractmethod
    def request_stacks_cards(self) -> bool:
        """request the status of all the cards"""
        pass
    

class ClientGameComms(ClientGameCommsInterface):
    _connection: ClientInterface
    _message_encoder: ClientMessageEncoder
    
    def __init__(self, logger: GameLogger, connection: ClientInterface) -> None:
        global client_logger
        client_logger = logger
        self._connection = connection
        self._message_encoder = ClientMessageEncoder(logger)

    def get_player_id(self) -> Players:
        """
        find out if we are player1 or player2
        
        Returns:
            bool: True if sending request succeeded
        """
        client_logger.info("sending player_id request")
        
        message = self._message_encoder.encode_request(ClientNetworkMessage.SEND_PLAYER_ID)
        
        # try:
        self._connection.send_message(message)
        # except Exception as e:
        #     log_message(f"error sending request: {e}")
        #     return Players.ERROR
            
        received_message: dict[str, ServerNetworkMessage | str | Players]  = {
            "type":"",
            "target":"",
            "value":""}
        while received_message["type"] != ServerNetworkMessage.SENDING_PLAYER_ID.value:
            message = self._connection.receive_message()
            received_message = loads(message)
            
            client_logger.debug(f"received message: {received_message}")
        
        # return Players(int(received_message["value"]))
        player = str(received_message["value"]).strip().upper()
        return Players[player]
            # return False
        
        # return True
        
    def request_stacks_cards(self) -> bool:
        """
        request the status of the cards on the card stacks
        
        Returns:
            bool: True if sending request succeeded
        """
        
        client_logger.info("client requesting stacks cards")
        
        # # empty the current stacks
        # self._stacks_cards = []
        
        # set the request
        message = self._message_encoder.encode_request(ClientNetworkMessage.SEND_STACKS_CARDS)
        
        try:
            self._connection.send_message(message)
        except Exception as e:
            client_logger.error(f"error sending request: {e}")
            return False
        
        return True
            
        
        # # receive the stacks cards
        # # TODO: adjust max size sometimes - this is a little bit of an overkill...
        # data = self._recv(10000)
        
        # # message = loads(data)

        # # if the stacks cards are not empty, print the stacks cards
        # # if len(self._stacks_cards) > 0:
        # if len(data) >0:
        #     info = loads(data)
        #     log_message(f"client stacks cards received: {info}")
        # else:
        #     log_message("no client stacks cards received")
            
    def server_quit(self) -> None:
        client_logger.info("client sending server notification of quuitting")
        
        message = self._message_encoder.encode_request(ClientNetworkMessage.QUIT)
        self._connection.send_message(message)
        # self._send_request(message)
       
        # self.disconnect()