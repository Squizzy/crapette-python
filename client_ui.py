import pygame
import os

from client_ui_cards import CardsUI
from client_ui_stacks_layout import StacksLayoutUI

from icecream import ic # type: ignore
ic.configureOutput(prefix='client_ui: ')
def log_message(msg:str) -> None:
    DEBUG = True
    if DEBUG:
        ic(msg)


# # dimensions of the game window
# GAME_WIDTH: int = 1024
# GAME_HEIGHT: int = 768
from constants import GAME_HEIGHT, GAME_WIDTH

# Initialising background colours
FELT_GREEN = (0, 96, 0) # felt dark green 
FELT_RED = (96, 0, 0) # felt dark red 
FELT_BLUE = (0, 0, 96) # felt dark blue 
YELLOW = (255, 255, 0) # yellow 

# # icon of the game
# IMAGES_DIR: str = os.path.dirname(os.path.abspath(__file__)) + "/img/"
# CARD_FACES_DIR: str = os.path.join(IMAGES_DIR, "card_faces")
# GAME_ICON_FILE: str = os.path.join(IMAGES_DIR, "two_backs_256x256.png")
# GAME_ICON: pygame.Surface = pygame.image.load(GAME_ICON_FILE)
# # GAME_ICON: pygame.Surface = pygame.image.load("img/two_backs_256x256.png")

from constants import IMAGES_DIR, CARD_FACES_DIR, GAME_ICON_FILE, GAME_ICON

class GameUIState:
    _is_moving: bool
    ...


class GameUI:
    _game_ui_state: GameUIState
    _cards_ui: CardsUI
    _stacks_ui_cards_layout: StacksLayoutUI
    
    _surface: pygame.Surface
    _table_colour: tuple[int, int, int]
    # _cards: CardsUI
    _stacks_layout: StacksLayoutUI
        
    def __init__(self):
        self._table_colour = FELT_GREEN
        self._pygame_init()
        self._surface = self._window_init()
        self._game_ui_state  = GameUIState()
        self._cards_ui = CardsUI(GAME_HEIGHT)
        self._stacks_layout = StacksLayoutUI(self._cards_ui)
        self._game_ui_state._is_moving = False
        

    @property
    def surface(self) -> pygame.Surface:
        return self._surface
    
    @surface.setter
    def surface(self, surface: pygame.Surface) -> None:
        self._surface = surface
    
    @property 
    def cards(self) -> CardsUI:
        return self._cards_ui
    
    @property 
    def stacks_layout(self) -> StacksLayoutUI:
        return self._stacks_layout

    @property
    def table_colour(self) -> tuple[int, int, int]:
        return self._table_colour

    def _pygame_init(self) -> None:
        """
        Initialize pygame
        """
        pygame.init()

    def _window_init(self) -> pygame.Surface:
        """
        Iniitialiise the game window surface

        Returns:
            pygame.Surface: the main display area for the game
        """
        # Set up the game window
        surface: pygame.Surface = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), pygame.RESIZABLE)

        # Set title of window
        pygame.display.set_caption("pygame title")

        # Set icon if window
        pygame.display.set_icon(GAME_ICON)

        # Change the background
        surface.fill(self.table_colour)
        
        return surface
    
    def _window_resize(self, width: int, height: int, other: int) -> None:   
        """
        Resize the game surface and reset its background colour
        Done here so that any game table element can be reset immediately.
        Makes it cleaner for the game loop

        Args:
            width (int): new width of the game window
            height (int): new height of the game window
            other (int | None): another parameter for the resize method
        """
        self._surface = pygame.display.set_mode((width, height), other)
        self._surface.fill(self.table_colour)
        self.stacks_layout.update_stacks_positions_and_sizes(width, height, self.cards)

    def _window_redraw(self):
        """
        Redraw the game screen
        """
        
        # place empty cards in the stacks positions
        self.stacks_layout.render_empty_stacks(self.surface, self.cards)
        
        # update the window
        pygame.display.flip()
