import pygame
import os

from constants import Players
from client_network import ClientConnection
from client_game_comms import ClientGameComms
from client_ui import GameUI
from game_logger import GameLogger

# from icecream import ic # type: ignore
# ic.configureOutput(prefix='client_pygame: ')
# def log_message(msg:str) -> None:
#     DEBUG = True
#     if DEBUG:
#         # ic(msg)
#         client_logger.debug(msg)

# dimensions of the game window
GAME_WIDTH: int = 1024
GAME_HEIGHT: int = 768

# Initialising background colours
FELT_GREEN = (0, 96, 0) # felt dark green 
FELT_RED = (96, 0, 0) # felt dark red 
FELT_BLUE = (0, 0, 96) # felt dark blue 
YELLOW = (255, 255, 0) # yellow 

# icon of the game
IMAGES_DIR: str = os.path.dirname(os.path.abspath(__file__)) + "/img/"
CARD_FACES_DIR: str = os.path.join(IMAGES_DIR, "card_faces")
GAME_ICON_FILE: str = os.path.join(IMAGES_DIR, "two_backs_256x256.png")
GAME_ICON: pygame.Surface = pygame.image.load(GAME_ICON_FILE)
# GAME_ICON: pygame.Surface = pygame.image.load("img/two_backs_256x256.png")

# dimensions of the image files
# objective value based on the graphics files used for th game
# TODO: this is for the png I am currently using
# -  eventually might be better to scan all files or store the values in a config file?
CARD_IMG_HEIGHT: int = 333
CARD_IMG_WIDTH: int = 234


# Stores a copy of the game state from the server
# Updates from the server
class GameState:
    _player_id: Players
    _stacks: dict[str, list[str]]
    _turn_player: int
    _is_running: bool
    
    def __init__(self) -> None:
        self._stacks = {
            "player_crapette":      [],
            "player_remainder":     [],
            "player_bin":           [],
            "player_tableau":       [],
            "player_foundation":    [],
            "opponent_crapette":    [],
            "opponent_remainder":   [],
            "opponent_bin":         [],
            "opponent_tableau":     [],
            "opponent_foundation":  [],
        }
        self._is_running = False
        
    @property
    def player_id(self) -> Players:
        return self._player_id
    
    @player_id.setter
    def player_id(self, player: Players) -> None:
        self._player_id = player
        


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
        self._game_ui = GameUI(client_logger)
        client_logger.info("client gameui instantiated")
        
        # connect to the server
        self._connection = ClientConnection(client_logger)
        self._connection.connect()
        client_logger.info("client connection established")
        
        # initialise the player id for this client
        # No this needs to happen in the game loop?
        # self._game_state.player_id = self._comm.request_player_id_from_server()
        # self._game_state.player_id = s
        # log_message(self._game_state.player_id.name)    
        
        self._game_comms = ClientGameComms(client_logger, self._connection)
        
        # get the cards from the server and assign them to the game state
        # No this need to happen in the game loop
        # stacks_cards_from_server = self._connection.server_get_stacks_cards()
        # self._game_comms.request_player_id()
        # stacks_cards = self._game_comms.
        
        self._game_state.player_id = self._game_comms.get_player_id()
        client_logger.debug(f"client player id acquired: {self._game_state.player_id.name}")
        
            
        # stacks_cards =  self._comm.server_get_stacks_cards()
        # # self._message_decoder = client_message_decoder()
        # crapette_stack = client_message_decoder.crapette_stack(message=stacks_cards)
        # # crapette_stack = self._message_decoder(stacks_cards)
        # print(crapette_stack)
        

    def _handle_events(self, event, rect) -> None:
        if event.type == pygame.QUIT:
            self._game_state._is_running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # print("Button Down")
            # rect = blit_card.get_rect()
            if rect.collidepoint(event.pos):
                client_logger.info("Collision detected")
                self._game_ui._game_ui_state._is_moving = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            # print("Button Up")
            self._game_ui._game_ui_state._is_moving = False
            
        elif event.type == pygame.MOUSEMOTION and self._game_ui._game_ui_state._is_moving:
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
        # def game_loop(surface: pygame.Surface, stacks_layout: StacksLayout, cards: Cards):
        # clock: pygame.time.Clock = pygame.time.Clock()

        blit_card = self._game_ui._cards_ui.faces["HQ"]
        # blit_card_width = card_faces["HQ"].get_width()
        # blit_card_height = card_faces["HQ"].get_height()
        # blit_card_angle = 0

        rect: pygame.Rect = blit_card.get_rect()
        # rect: pygame.Rect = card_faces["HQ"].get_rect()
        # surface.blit(blit_card, (100, 100))

        # color = FELT_GREEN
        
        
        # A card or stack is being displaced
        self._game_ui._game_ui_state._is_moving = False

        # Set the game running state
        self._game_state._is_running = True
        
        # Game loop 
        while self._game_state._is_running:
            
            # Handle events
            for event in pygame.event.get():
                self._handle_events(event, rect)
                
                
            # self.get_stacks_cards()
            # self.get_stacks_cards_from_server()
            self._handle_graphics()
            # self._window_redraw()
            
            # # place empty cards in the stacks positions
            # self.stacks_layout.render_empty_stacks(self.surface, self.cards)
            
            # # update the window
            # # pygame.display.update()
            # pygame.display.flip()
            
            # delay
            pygame.time.delay(100)
            
            # Make a circle
            # pygame.draw.circle(surface, (FELT_BLUE), (GAME_WIDTH/2, GAME_HEIGHT/2), 75)

            # Make a rectangle
            # this_rect = pygame.draw.rect(surface, color=YELLOW, rect=pygame.Rect(30, 30, 60, 60))

            # print("blitting")
            # surface.blit(blit_card, rect)

            # scaling
            # blit_card_width = int(blit_card_width * 0.99)
            # blit_card_height = int(blit_card_height * 0.99)
            # blit_card = pygame.transform.smoothscale(card_faces["HQ"], (blit_card_width, blit_card_height))

            # rotating
            # blit_card_angle = blit_card_angle + 3
            # blit_card = pygame.transform.rotate(blit_card, blit_card_angle)
            # card_faces["HQ"] = pygame.transform.scale(card_faces["HQ"], (int(card_faces["HQ"].get_size()[0]*0.99), int(card_faces["HQ"].get_size()[1]*0.99)))

            # surface.blit(card_faces["EC"], (120, 120))



            # clock.tick(3000)

        self._game_comms.server_quit()
        pygame.quit()

# def server_get_stacks_cards():
#     #TODO: Implement the server_get_stacks_cards function - use get_stacks_cards_from_server() instead?
#     ...
    
def player_stacks_init(player: int):

    # create the stacks dictionary
    stacks_cards: dict[str, list[str]] = {
        "player_crapette":      [],
        "player_remainder":     [],
        "player_bin":           [],
        "player_tableau":       [],
        "player_foundation":    [],
        "opponent_crapette":    [],
        "opponent_remainder":   [],
        "opponent_bin":         [],
        "opponent_tableau":     [],
        "opponent_foundation":  [],
    }
    
    # server_stacks_cards = server_get_stacks_cards()
    # TODO: convert the server_stacks_cards to the stacks_cards dictionary
    # return stacks_cards







def update_stacks(surface: pygame.Surface):
    #TODO: Implement the update_stacks function
    ...




if __name__ == "__main__":
    
    client_logger =  GameLogger("client_logger")
    
    game: Game = Game()
    # pygame_init()
    # surface: pygame.Surface = window_init()
    # cards: Cards = Cards(GAME_HEIGHT)
    # stacks_layout: StacksLayout = StacksLayout(cards)
    # stacks_cards: dict[str, list[str]] = player_stacks_init(1)
    # load_card_faces()
    # game_loop(game.surface, game.stacks_layout, game.cards)
    game.game_loop()
