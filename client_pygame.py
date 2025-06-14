import pygame
import time

# from constants import Players
from client_network import ClientConnection
from client_game_comms import ClientGameComms
from client_ui import GameUI
from client_game_state import GameState

from game_logger import GameLogger, DebugLevel
client_logger: GameLogger = GameLogger("client_pygame", level=DebugLevel.client_pygame.value)


class Game:
    _game_state: GameState
    _game_ui: GameUI
    _connection: ClientConnection
    _game_comms: ClientGameComms

    def __init__(self) -> None:
        
        # Instantiate the game state
        self._game_state = GameState()
        client_logger.info("client gamestate instantiated")
        
        # Instantiate the game UI
        self._game_ui = GameUI(self._game_state)
        client_logger.info("client gameui instantiated")
        
        
        # TODO: Move the network stuff to a network_state
        # connect to the server
        self._connection = ClientConnection()
        self._connection.connect()
        client_logger.info("client connection established")
        
        # initialise the player id for this client
        # No this needs to happen in the game loop?
        # self._game_state.player_id = self._comm.request_player_id_from_server()
        # self._game_state.player_id = s
        # log_message(self._game_state.player_id.name)    
        
        self._game_comms = ClientGameComms(self._connection)
        
        # get the cards from the server and assign them to the game state
        # No this need to happen in the game loop
        # stacks_cards_from_server = self._connection.server_get_stacks_cards()
        # self._game_comms.request_player_id()
        # stacks_cards = self._game_comms.
        
        self._game_comms.request_player_id()
        self._game_state.player_id = self._game_comms.retrieve_player_id()
        client_logger.debug(f"client player id acquired: {self._game_state.player_id.name}")
        
        self._game_comms.request_stacks_cards()
        self._game_state._stacks_cards = self._game_comms.retrieve_stacks_cards()
        
    def _handle_events(self, event) -> None:
        
        rect = pygame.Rect(0, 0, 0, 0)
        
        if event.type == pygame.QUIT:
            self._game_state._is_running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos:
                client_logger.debug(self._game_ui.check_for_collision(event))
            # print("Button Down")
            # rect = blit_card.get_rect()
            # if rect.collidepoint(event.pos):
            #     client_logger.info("Collision detected")
            #     self._game_ui._ui_game_state._is_moving = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            # client_logger.debug("Button Up")
            self._game_ui._ui_game_state._is_moving = False
            
        elif event.type == pygame.MOUSEMOTION and self._game_ui._ui_game_state._is_moving:
            ...
            # print(f"Mouse Move: {rect.x=}, {rect.y=}")
            rect.move_ip(event.rel)
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                client_logger.info("Escape Key detected")
                self._game_state._is_running = False

            
        elif  event.type == pygame.VIDEORESIZE:
            self._game_ui._window_resize(event.w, event.h, pygame.RESIZABLE)
            
        else:
            pass

    def _handle_graphics(self) -> None:
        self._game_ui._window_redraw()

    def game_loop(self) -> None:
        """
        The main game loop

        """
        
        # A card or stack is being displaced
        self._game_ui._ui_game_state._is_moving = False

        # Set the game running state
        self._game_state._is_running = True
        
        # previous = time.time()
        
        # Game loop 
        while self._game_state._is_running:
            # current = time.time()
            # elapsed = current - previous
            # previous = current
            
            
            # Handle events
            for event in pygame.event.get():
                self._handle_events(event)

            # Handle graphics
            self._handle_graphics()

            
            # delay the game loop so it runs once every 16 milliseconds
            time.sleep(0.016)
        
        # for now if the game loop is finished, then quit the game    
        self._game_comms.server_quit()
        pygame.quit()


if __name__ == "__main__":
        
    game: Game = Game()
    game.game_loop()
