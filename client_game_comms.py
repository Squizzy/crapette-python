from abc import ABC, abstractmethod
from json import loads

from constants import Players
from client_network import ClientInterface
from network_messages import ClientNetworkMessage, ServerNetworkMessage
# from message_encoder import encode_request
from client_msg_encoder import ClientMessageEncoder
from client_msg_decoder import ClientMessageDecoder
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
    def request_player_id(self) -> bool:
        """Request the player ID from the server"""
        pass

    @abstractmethod
    def retrieve_player_id(self) -> Players:
        """Recover the player id as sent by the server"""
        pass

    @abstractmethod
    def request_stacks_cards(self) -> bool:
        """Request the current stacks cards from the server"""
        pass
    
    @abstractmethod
    def retrieve_stacks_cards(self) -> dict[str, list[str]]:
        """Retrieve the stacks cards as sent by server"""
        pass
    
    @abstractmethod
    def server_quit(self) -> None:
        """Inform the server that client is quitting"""
        pass

    

class ClientGameComms(ClientGameCommsInterface):
    _connection: ClientInterface
    _message_encoder: ClientMessageEncoder
    _message_decoder: ClientMessageDecoder
    
    def __init__(self, logger: GameLogger, connection: ClientInterface) -> None:
        global client_logger
        client_logger = logger
        self._connection = connection
        self._message_encoder = ClientMessageEncoder(logger)
        self._message_decoder = ClientMessageDecoder(logger)

    def request_player_id(self) -> bool:
        """Request the server to send the player ID

        Returns:
            bool: True if request sent fine
        """
        
        client_logger.info("sending player_id request")
        
        message = self._message_encoder.encode_request(ClientNetworkMessage.SEND_PLAYER_ID)
        
        try:
            self._connection.send_message(message)
        except Exception as e:
            client_logger.error(f"error sending request: {e}")
            return False
        
        client_logger.info("player_id request sent")
        return True

    def retrieve_player_id(self) -> Players:
        """
        retrieve the player_id sent by the server
        
        Returns:
            Players: The player ID as sent by the server
        """

        client_logger.info("retrieving the player_id as sent by the server")
        
        received_type: ServerNetworkMessage = ServerNetworkMessage.NONE
        # received_value: Players = Players.ERROR
        
        while received_type != ServerNetworkMessage.SENDING_PLAYER_ID:
            message = self._connection.receive_message()
            received_type = ServerNetworkMessage(loads(message)["type"])
                    
        # received_value = loads(message)["value"]

        # try:
        #     player = Players[str(received_value)]
        # except KeyError as e:
        #     client_logger.error(f"received player_id is not a valid player id: {e}")
        #     return Players.ERROR
        
        # client_logger.debug(f"{player=}")
        
        player = self._message_decoder.decode_player_id(message)
        
        return player

        
    def request_stacks_cards(self) -> bool:
        """
        request the status of the cards on the card stacks
        
        Returns:
            bool: True if sending request succeeded
        """
        
        client_logger.info("client requesting stacks cards")
        
        # set the request
        message = self._message_encoder.encode_request(ClientNetworkMessage.SEND_STACKS_CARDS)
        
        try:
            self._connection.send_message(message)
        except Exception as e:
            client_logger.error(f"error sending request: {e}")
            return False

        client_logger.info("client request sent")
        return True
            
    def retrieve_stacks_cards(self) -> dict[str, list[str]]:
        
        client_logger.info("retrieving the stacks cards as sent by the server")
        
        received_type: ServerNetworkMessage = ServerNetworkMessage.NONE
        # received_value: dict[str, list[str]] = {}
        
        # Wait until the proper message is received
        # TODO: This needs to be better : timeout, resend request etc...
        while received_type != ServerNetworkMessage.SENDING_STACKS_CARDS:
            message = self._connection.receive_message()
            received_type = ServerNetworkMessage(loads(message)["type"])
            
            # client_logger.debug(f"{received_type=}")
        
        # # Extract the stacks cards from the received message
        # received_value = loads(message)["value"]

        # # check that data was received, if not it is a problem
        # if len(received_value) > 0:
        #     stacks_cards = received_value
        # else:
        #     client_logger.error("received stacks cards is empty")
        #     return {}
        
        # client_logger.debug(f"retrieved stacks cards: {stacks_cards}")
        
        stacks_cards = self._message_decoder.decode_stacks_cards(message)
        
        return stacks_cards
        
        
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
        
       
        
        
    # def get_stacks_cards(self) -> dict[str, list[str]]:
    #     """
    #     request the status of the cards on the card stacks
        
    #     Returns:
    #         bool: True if sending request succeeded
    #     """
        
    #     client_logger.info("client requesting stacks cards")
        
    #     # # empty the current stacks
    #     # self._stacks_cards = []
        
    #     # set the request
    #     message = self._message_encoder.encode_request(ClientNetworkMessage.SEND_STACKS_CARDS)
        
    #     try:
    #         self._connection.send_message(message)
    #     except Exception as e:
    #         client_logger.error(f"error sending request: {e}")
    #     #     return False
        
    #     # return True
            
    #     received_data = 1
        
    #     return {}
        
        
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