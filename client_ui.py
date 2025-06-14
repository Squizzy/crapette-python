import pygame
# import os

from constants import GAME_HEIGHT, GAME_WIDTH
from constants import GAME_ICON_FILE
from constants import TableColours
# from constants import IMAGES_DIR, CARD_FACES_DIR
from client_ui_cards import CardsUI
from client_ui_stacks_layout import StacksLayoutUI
from client_ui_game_state import UIGameState
from client_game_state import GameState

from game_logger import GameLogger, DebugLevel
client_logger: GameLogger = GameLogger("client_ui", level=DebugLevel.client_ui.value)


class GameUI:
    _game_state: GameState
    _ui_game_state: UIGameState
    _cards_ui: CardsUI
    _stacks_ui_cards_layout: StacksLayoutUI
    
    # _table_colour: tuple[int, int, int]
    _stacks_layout: StacksLayoutUI
        
    def __init__(self, game_state: GameState):
        
        # link the client game_state
        self._game_state = game_state
        
        # Instantiate the UI game state
        self._ui_game_state  = UIGameState()
        client_logger.info("Game UI state instantiated")
        
        # Instantiate the window surface and set its background color
        self._ui_game_state.table_colour = TableColours.FELT_GREEN
        self._pygame_init()
        self._window_init()
        client_logger.info("SDL window instantiated")
        
        # Instantiate the cards UI and the stacks layout UI
        self._cards_ui = CardsUI(game_state, self._ui_game_state)
        client_logger.info("Cards UI instantiated")
        
        self._stacks_layout = StacksLayoutUI(self._ui_game_state)
        client_logger.info("Stacks UI instantiated")
        
        self._ui_game_state.on_window_resize(self._ui_game_state.window)      


    def _pygame_init(self) -> None:
        """
        Initialize pygame
        """
        pygame.init()

    def _window_init(self):
        """
        Iniitialiise the game window surface

        Returns:
            pygame.Surface: the main display area for the game
        """
        # Set up the game window
        self._ui_game_state.window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), pygame.RESIZABLE)

        # Set title of window
        pygame.display.set_caption("pygame title")

        # Set icon if window
        self._ui_game_state.game_icon = pygame.image.load(GAME_ICON_FILE)
        pygame.display.set_icon(self._ui_game_state.game_icon)

        # Change the background
        self._ui_game_state.window.fill(self._ui_game_state.table_colour)

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
        surface: pygame.Surface = pygame.display.set_mode((width, height), other)
        surface.fill(self._ui_game_state.table_colour)
        self._ui_game_state.on_window_resize(surface)

    def _window_redraw(self):
        """
        Redraw the game screen
        """
        
        # place empty cards in the stacks positions
        self._stacks_layout.render_empty_stacks()
        
        # place the cards on the stacks (initially, 13 on the crapette, 1 on each own tableau and rest in remainder)
        self._cards_ui.place_stacks_cards()
        
        # update the window
        pygame.display.flip()

    def check_for_collision(self, event: pygame.event.Event) -> str:
        
        area: str = "table" # default value: hit the table
        card_found = -1
        
        collision_checklist_order = [
            "player_crapette",
            "player_remainder",
            "player_bin",
            "opponent_crapette",
            "opponent_remainder",
            "opponent_bin",
            "player_foundation0",
            "player_foundation1",
            "player_foundation2",
            "player_foundation3",
            "opponent_foundation0",
            "opponent_foundation1",
            "opponent_foundation2",
            "opponent_foundation3",
        ]
        
        tableau_checklist_order = [
            "player_tableau0",
            "player_tableau1",
            "player_tableau2",
            "player_tableau3",
            "opponent_tableau0",
            "opponent_tableau1",
            "opponent_tableau2",
            "opponent_tableau3",
        ]
        
        #TODO: if there is no card on the stack, the collision should be with the table.
        # check the value of the card __str__ for this
        
        found_collision: bool = False
        for stack in collision_checklist_order:
            for rect, card_num, card in self._ui_game_state.collision_areas[stack]:
                if rect.collidepoint(event.pos):
                    area = stack
                    card_found = 0
                    found_collision = True
        
        if not found_collision:
            # Check each tableau in order
            for tableau in tableau_checklist_order:
                if found_collision:
                    break
                # Get the list of cards on this tableau
                cards_list = self._ui_game_state.tableau_cards_locations[tableau].copy()
                # Reverse the list of cards so the 13th (12th) is at position 0, the one we want to test first
                cards_list.reverse()
                # get the x position of this card
                for x, card in cards_list:
                    # Find the rect of this card, 
                    # for this we need the tableau stack rect, and substitute the x
                    # first, get the base pos of the stack
                    tableau_collision = self._ui_game_state.collision_areas[tableau]
                    # create a variable that inherits these coordinates
                    card_collision: pygame.Rect = tableau_collision[0][0] #0th item on the list is base pos of stack, the other 0 represent the Rect of it 
                    # replace the x with the one of the card
                    card_collision.x = x
                    if card_collision.collidepoint(event.pos):
                        area = stack
                        found_collision = True
                        card_found = card_num
                        break
            
            
        # for key, list_of_Rects in self._ui_game_state.collision_areas.items():
            # for rect, card_num, card in list_of_Rects:
            #     if rect.collidepoint(event.pos):
            #         area = key
                    
        return f"{event.pos=} - Hit: {area=} {card_found=}"
