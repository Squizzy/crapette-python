from player import Player
from constants import Players
from server_network import ServerConnection
from json import dumps
from icecream import ic # type: ignore


# from gamestates import GameStates

DEBUG: bool = True
ic.configureOutput(prefix = "pygame-server: ")
def log_message(message: str):
    if DEBUG:
        ic(message)

class Game:
    _player1: Player
    _player2: Player
    
    def __init__(self):
        self._player1 = Player(Players.PLAYER1)
        self._player2 = Player(Players.PLAYER2)
        
    def get_player_stacks(self, player_num: Players) -> dict[str, list[str]]:
        if player_num == Players.PLAYER1:
            return {
                "player_crapette": self._player1._crapette.to_dict(),
                "player_remainder": self._player1._remainder.to_dict(),
                "player_bin": self._player1._bin.to_dict(),
                "player_tableau0": self._player1._tableau._TableauStacks[0].to_dict(),
                "player_tableau1": self._player1._tableau._TableauStacks[1].to_dict(),
                "player_tableau2": self._player1._tableau._TableauStacks[2].to_dict(),
                "player_tableau3": self._player1._tableau._TableauStacks[3].to_dict(),
                "player_foundation0": self._player1._foundation._FoundationStacks[0].to_dict(),
                "player_foundation1": self._player1._foundation._FoundationStacks[1].to_dict(),
                "player_foundation2": self._player1._foundation._FoundationStacks[2].to_dict(),
                "player_foundation3": self._player1._foundation._FoundationStacks[3].to_dict(),
            }
        elif player_num == Players.PLAYER2:
            return {
                "player_crapette": self._player2._crapette.to_dict(),
                "player_remainder": self._player2._remainder.to_dict(),
                "player_bin": self._player2._bin.to_dict(),
                "player_tableau0": self._player2._tableau._TableauStacks[0].to_dict(),
                "player_tableau1": self._player2._tableau._TableauStacks[1].to_dict(),
                "player_tableau2": self._player2._tableau._TableauStacks[2].to_dict(),
                "player_tableau3": self._player2._tableau._TableauStacks[3].to_dict(),
                "player_foundation0": self._player2._foundation._FoundationStacks[0].to_dict(),
                "player_foundation1": self._player2._foundation._FoundationStacks[1].to_dict(),
                "player_foundation2": self._player2._foundation._FoundationStacks[2].to_dict(),
                "player_foundation3": self._player2._foundation._FoundationStacks[3].to_dict(),
            }
        else:
            raise ValueError("Invalid player number")
        
    def get_players_cards(self) -> dict[Players, dict[str, list[str]]]:
        return {
            "Players.PLAYER1": self.get_player_stacks(Players.PLAYER1),
            "Players.PLAYER2": self.get_player_stacks(Players.PLAYER2)
        }
        

if __name__ == "__main__":
    
    log_message("Starting server")
    game_server = Game()
    log_message("Game server started")
    
    log_message("getting players cards")
    stacks_data = game_server.get_players_cards()
    log_message(f"stacks_data: {stacks_data}")
    
    JSON_stacks_data = dumps(stacks_data)
    log_message(f"JSON_stacks_data:  {JSON_stacks_data}")
    log_message(f"{len(JSON_stacks_data)}")
    
    log_message("establishing network server")
    server_connection = ServerConnection()
    
    log_message("starting network server")
    server_connection.start_server()
    
    log_message("accepting connection")
    server_connection.accept_connection()
    
    log_message("listening waiting for client requests")
    data_request = server_connection.listen_for_requests()
    
    log_message(f"data_request:  {data_request}")
    if data_request == "send_stacks_cards":
        server_connection.send_players_stacks(JSON_stacks_data)
        log_message("sent stacks cards")
        
    log_message("closing network server")
    server_connection.close_connection()