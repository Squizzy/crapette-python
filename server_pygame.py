import time

from player import Player
from constants import Players
from server_network import  ServerConnection
from server_game_comms import ServerGameComms
from network_messages import ClientNetworkMessage
from server_msg_decoder import ServerMessageDecoder
from game_logger import GameLogger


server_logger: GameLogger

# from icecream import ic # type: ignore
# ic.configureOutput(prefix="server_pygame: ")
# def log_message(message: str):
#     # enable debug messages
#     DEBUG = True
#     if DEBUG:
#         ic(message)


class GameState:
    _instance: 'GameState | None' = None
    _initialised: bool = False
    
    _player_1_socket: int
    _player_2_socket: int
    _stacks_cards: dict[str, dict[str, list[str]]]
    _is_player1_turn: bool
    
    _is_running: bool

    # Create a singleton to ensure only one instance of GameState exists
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameState, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not self._initialised:
            self._init_stacks_cards()
            self._initialised  = True
            self._is_running = False
        
    def _init_stacks_cards(self) -> None:
        self._stacks_cards = {
            
            Players.PLAYER0.name: {
                "crapette":      [],
                "remainder":     [],
                "bin":           [],
                "tableau0":      [],
                "tableau1":      [],
                "tableau2":      [],
                "tableau3":      [],
                "foundation0":   [],
                "foundation1":   [],
                "foundation2":   [],
                "foundation3":   [],
            },
            Players.PLAYER1.name: {
        
                "crapette":      [],
                "remainder":     [],
                "bin":           [],
                "tableau0":      [],
                "tableau1":      [],
                "tableau2":      [],
                "tableau3":      [],
                "foundation0":   [],
                "foundation1":   [],
                "foundation2":   [],
                "foundation3":   [],
            },
        }
        self._is_player1_turn = True
    
    @property
    def is_running(self) -> bool:
        return self._is_running
    
    @is_running.setter
    def is_running(self, value:bool) -> None:
        self._is_running = value
    
    @property
    def stacks_cards(self) -> dict[str, dict[str, list[str]]]:
        return self._stacks_cards
    
    @stacks_cards.setter
    def stacks_cards(self, stacks_cards: dict[str, dict[str, list[str]]]) -> None:
        for player in stacks_cards:
            for stack in stacks_cards[player]:
                for card in stack:
                    self._stacks_cards[player][stack].append(card)
        
    def update_stacks_cards(self, player0_stacks: Player, player1_stacks: Player):

            self._stacks_cards[Players.PLAYER0.name]["crapette"] = player0_stacks.crapette.to_list()
            self._stacks_cards[Players.PLAYER0.name]["remainder"] = player0_stacks.remainder.to_list()
            self._stacks_cards[Players.PLAYER0.name]["bin"] = player0_stacks.bin.to_list()
            self._stacks_cards[Players.PLAYER0.name]["tableau0"] = player0_stacks.tableau0.to_list()
            self._stacks_cards[Players.PLAYER0.name]["tableau1"] = player0_stacks.tableau1.to_list()
            self._stacks_cards[Players.PLAYER0.name]["tableau2"] = player0_stacks.tableau2.to_list()
            self._stacks_cards[Players.PLAYER0.name]["tableau3"] = player0_stacks.tableau3.to_list()
            self._stacks_cards[Players.PLAYER0.name]["foundation0"] = player0_stacks.foundation0.to_list()
            self._stacks_cards[Players.PLAYER0.name]["foundation1"] = player0_stacks.foundation1.to_list()
            self._stacks_cards[Players.PLAYER0.name]["foundation2"] = player0_stacks.foundation2.to_list()
            self._stacks_cards[Players.PLAYER0.name]["foundation3"] = player0_stacks.foundation3.to_list()
            server_logger.debug(f"player0 crapette updated: {self._stacks_cards[Players.PLAYER0.name]['crapette']}")
            
            self._stacks_cards[Players.PLAYER1.name]["crapette"] = player1_stacks.crapette.to_list()
            self._stacks_cards[Players.PLAYER1.name]["remainder"] = player1_stacks.remainder.to_list()
            self._stacks_cards[Players.PLAYER1.name]["bin"] = player1_stacks.bin.to_list()
            self._stacks_cards[Players.PLAYER1.name]["tableau0"] = player1_stacks.tableau0.to_list()
            self._stacks_cards[Players.PLAYER1.name]["tableau1"] = player1_stacks.tableau1.to_list()
            self._stacks_cards[Players.PLAYER1.name]["tableau2"] = player1_stacks.tableau2.to_list()
            self._stacks_cards[Players.PLAYER1.name]["tableau3"] = player1_stacks.tableau3.to_list()
            self._stacks_cards[Players.PLAYER1.name]["foundation0"] = player1_stacks.foundation0.to_list()
            self._stacks_cards[Players.PLAYER1.name]["foundation1"] = player1_stacks.foundation1.to_list()
            self._stacks_cards[Players.PLAYER1.name]["foundation2"] = player1_stacks.foundation2.to_list()
            self._stacks_cards[Players.PLAYER1.name]["foundation3"] = player1_stacks.foundation3.to_list()
            server_logger.debug(f"player1 crapette updated: {self._stacks_cards[Players.PLAYER1.name]['crapette']}")
        

class Game:
    _game_state: GameState
    _stacks_data:  dict[str, list[str]]
    _player0: Player
    _player1: Player
    _conn:    ServerConnection
    _game_comms: ServerGameComms
    _message_decoder: ServerMessageDecoder
    
    def __init__(self):
        # initiate the players and their game packs and stacks
        self._player0 = Player(Players.PLAYER0)
        self._player1 = Player(Players.PLAYER1)
        
        # create the game state
        self._game_state = GameState()
        server_logger.info("server game state initialised")
        
        self._message_decoder = ServerMessageDecoder(server_logger)
        
        # load the player cards into the game state
        self._stacks_data = self._get_players_cards()
        server_logger.info("cards dealt")
        server_logger.warning("cards currently not shuffled")

        # log_message("establishing network server")
        # self._conn = ServerConnection()
        
        # log_message("starting network server")
        # self._conn.start_server()
        
        # log_message("accepting connection")
        # self._conn.accept_connection()
        
        # log_message("listening waiting for client requests")
        # try:
        #     data_request = self._conn.listen_for_requests()
        # except Exception as e:
        #     log_message(f"Error in listening for requests: {e}")
        #     self._conn.close_connection()
        #     raise
        
        self._conn = ServerConnection(server_logger)
        server_logger.info("Instantiating network server")
        
        self._conn.start()
        server_logger.info("network server started")
        
        self._game_comms = ServerGameComms(server_logger, self._conn)
        server_logger.info("server game comms initialised")
        
        self._conn.accept_connection()
        server_logger.info("connected to client")

        self._game_loop()
        server_logger.info("game loop ended")
    
    
    def _get_players_cards(self) ->  dict[str, dict[str, list[str]]]:

        self._game_state.update_stacks_cards(self._player0, self._player1)
        server_logger.debug(f"{self._game_state.stacks_cards}")

        return self._game_state.stacks_cards

    def _process_messages_received(self, msg: str, client: Players):
        
        # server_logger.debug(f"received message: {msg}")
        # server_logger.debug(f"received message: {ClientNetworkMessage.QUIT.value}")
        # message = loads(msg)["type"]
        message = self._message_decoder.decode_request(msg)
        
        # log_message(f"received message: {message}")
        # log_message(f"received message: {ClientNetworkMessage.SEND_PLAYER_ID}")
        # log_message(f"received message: {message["type"]}")
        # log_message(f"received message: {ClientNetworkMessage.SEND_PLAYER_ID.name}")
        if message == ClientNetworkMessage.SEND_PLAYER_ID:
            self._game_comms.send_player_id(client)
                
        elif message == ClientNetworkMessage.SEND_STACKS_CARDS:
            self._game_comms.send_stacks_cards(client, self._game_state._stacks_cards)
            # return "send_stacks_cards"
            
        elif message == ClientNetworkMessage.QUIT:
            # self._acknowledge("quit accepted")
            server_logger.info("Ok, about to quit")
            self._game_state.is_running = False
        ...


    def _quit(self) -> None:
        self._game_state.is_running = False
        self._conn.stop()
        server_logger.info("server stopped")


    def _game_loop(self):
        self._game_state.is_running =  True
        
        while self._game_state.is_running:
            
            for client in self._conn.connected_clients:
                # received_message = ""
                while True:
                    received_message = self._conn.receive_message_from_client(client)
                    if not received_message:
                        break
                    self._process_messages_received(received_message, client)

            # if received_message == ClientNetworkMessage.SEND_PLAYER_ID.name:
            #     self._game_comms.send_player_id(Players.PLAYER1)
                
            # elif received_message == ClientNetworkMessage.SEND_STACKS_CARDS.name:
            #     self._send_stacks_cards()
            #     # return "send_stacks_cards"
            
            # elif received_message == ClientNetworkMessage.QUIT.name:
            #     # self._acknowledge("quit accepted")
            #     self.close_connection()
            
            # else:
            #     continue
            time.sleep(0.016)
            
        self._quit()
        server_logger.info("server game loop ended")



if __name__ == "__main__":
    server_logger = GameLogger("server_logger")
    
    server_logger.info("Starting server")
    game_server = Game()
    server_logger.info("Game server started")
    
    # game_state = GameState()
    # log_message("server game state initialised")
    
    # log_message("getting players cards")
    # stacks_data = game_server.get_players_cards()
    # log_message(f"stacks_data: {stacks_data}")
    
    # game_state.update_stacks_cards_crapette(stacks_data)
    
    
    # JSON_stacks_data = dumps(stacks_data)
    # # log_message(f"JSON_stacks_data:  {JSON_stacks_data}")
    # log_message(f"{len(JSON_stacks_data)}")
    
    # log_message("establishing network server")
    # server_connection = ServerConnection()
    
    # log_message("starting network server")
    # server_connection.start_server()
    
    # log_message("accepting connection")
    # server_connection.accept_connection()
    
    # log_message("listening waiting for client requests")
    # data_request = server_connection.listen_for_requests()
    
    # log_message(f"data_request:  {data_request}")
    # if data_request == "send_stacks_cards":
    #     server_connection.send_players_stacks(JSON_stacks_data)
    #     log_message("sent stacks cards")
        
    # log_message("closing network server")
    # server_connection.close_connection()