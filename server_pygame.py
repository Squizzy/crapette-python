from player import Player
from constants import Players
from server_network import  ServerConnection
from server_game_comms import ServerGameComms
from network_messages import ClientNetworkMessage




from icecream import ic # type: ignore
ic.configureOutput(prefix="server_pygame: ")
def log_message(message: str):
    # enable debug messages
    DEBUG = True
    if DEBUG:
        ic(message)


class GameState:
    _instance: 'GameState | None' = None
    _initialised: bool = False
    
    _player_1_socket: int
    _player_2_socket: int
    _stacks_cards: dict[str, list[str]]
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
            "player1_crapette":      [],
            "player1_remainder":     [],
            "player1_bin":           [],
            "player1_tableau0":      [],
            "player1_tableau1":      [],
            "player1_tableau2":      [],
            "player1_tableau3":      [],
            "player1_foundation0":   [],
            "player1_foundation1":   [],
            "player1_foundation2":   [],
            "player1_foundation3":   [],
            
            "player2_crapette":      [],
            "player2_remainder":     [],
            "player2_bin":           [],
            "player2_tableau0":      [],
            "player2_tableau1":      [],
            "player2_tableau2":      [],
            "player2_tableau3":      [],
            "player2_foundation0":   [],
            "player2_foundation1":   [],
            "player2_foundation2":   [],
            "player2_foundation3":   [],
        }
        self._is_player1_turn = True
        
    def update_stacks_cards(self, player1_card_stacks: Player, player2_card_stacks: Player):

            self._stacks_cards["player1_crapette"] = player1_card_stacks._crapette.to_list()
            self._stacks_cards["player1_remainder"] = player1_card_stacks._remainder.to_list()
            self._stacks_cards["player1_bin"] = player1_card_stacks._bin.to_list()
            self._stacks_cards["player1_tableau0"] = player1_card_stacks._tableau0.to_list()
            self._stacks_cards["player1_tableau1"] = player1_card_stacks._tableau1.to_list()
            self._stacks_cards["player1_tableau2"] = player1_card_stacks._tableau2.to_list()
            self._stacks_cards["player1_tableau3"] = player1_card_stacks._tableau3.to_list()
            self._stacks_cards["player1_foundation0"] = player1_card_stacks._foundation0.to_list()
            self._stacks_cards["player1_foundation1"] = player1_card_stacks._foundation1.to_list()
            self._stacks_cards["player1_foundation2"] = player1_card_stacks._foundation2.to_list()
            self._stacks_cards["player1_foundation3"] = player1_card_stacks._foundation3.to_list()
            log_message(f"player1_crapette updated: {self._stacks_cards['player1_crapette']}")
            
            self._stacks_cards["player2_crapette"] = player2_card_stacks._crapette.to_list()
            self._stacks_cards["player2_remainder"] = player2_card_stacks._remainder.to_list()
            self._stacks_cards["player2_bin"] = player2_card_stacks._bin.to_list()
            self._stacks_cards["player2_tableau0"] = player2_card_stacks._tableau0.to_list()
            self._stacks_cards["player2_tableau1"] = player2_card_stacks._tableau1.to_list()
            self._stacks_cards["player2_tableau2"] = player2_card_stacks._tableau2.to_list()
            self._stacks_cards["player2_tableau3"] = player2_card_stacks._tableau3.to_list()
            self._stacks_cards["player2_foundation0"] = player2_card_stacks._foundation0.to_list()
            self._stacks_cards["player2_foundation1"] = player2_card_stacks._foundation1.to_list()
            self._stacks_cards["player2_foundation2"] = player2_card_stacks._foundation2.to_list()
            self._stacks_cards["player2_foundation3"] = player2_card_stacks._foundation3.to_list()
            log_message(f"player2_crapette updated: {self._stacks_cards['player2_crapette']}")
        

class Game:
    _game_state: GameState
    _stacks_data:  dict[str, list[str]]
    _player1: Player
    _player2: Player
    _conn:    ServerConnection
    _game_comms: ServerGameComms
    
    def __init__(self):
        # initiate the players and their game packs and stacks
        self._player1 = Player(Players.PLAYER1)
        self._player2 = Player(Players.PLAYER2)
        
        # create the game state
        self._game_state = GameState()
        log_message("server game state initialised")
        
        # load the player cards into the game state
        self._stacks_data = self._get_players_cards()

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
        
        self._conn = ServerConnection()
        log_message("Instantiating network server")
        
        self._conn.start()
        log_message("network server started")
        
        self._game_comms = ServerGameComms(self._conn)
        log_message("server game comms initialised")
        
        self._conn.accept_connection()
        log_message("connected to client")

        self._game_loop()
        log_message("game loop ended")
    
    
    def _get_players_cards(self) ->  dict[str, list[str]]:

        self._game_state.update_stacks_cards(self._player1, self._player2)
        log_message(f"{self._game_state._stacks_cards}")

        return self._game_state._stacks_cards

    def _process_messages_received(self, message: ClientNetworkMessage, client: Players):
        if message == ClientNetworkMessage.SEND_PLAYER_ID.name:
            self._game_comms.send_player_id(client)
                
        elif message == ClientNetworkMessage.SEND_STACKS_CARDS.name:
            self._game_comms.send_stacks_cards(client, self._game_state._stacks_cards)
            # return "send_stacks_cards"
            
        elif message == ClientNetworkMessage.QUIT.name:
            # self._acknowledge("quit accepted")
            self._game_state._is_running = False
        ...


    def _quit(self) -> None:
        self._game_state._is_running = False
        self._conn.stop()
        log_message("server stopped")


    def _game_loop(self):
        self._game_state._is_running =  True
        
        while self._game_state._is_running:
            
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
            
        self._quit()
        log_message("server game loop ended")



if __name__ == "__main__":
    
    log_message("Starting server")
    game_server = Game()
    log_message("Game server started")
    
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