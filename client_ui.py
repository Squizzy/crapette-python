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
        
        # TODO: Move to the correct location
        client_logger.warning("move fill_card_position call to the correct location")
        self._cards_ui.fill_card_positions()

        # place empty cards in the stacks positions
        self._stacks_layout.render_empty_stacks()   
        
        # stacks location as rectangles declared, not sprites like empty_stacks do
        # might keep it as looks ok
        self._stacks_layout.render_stacks_locations()
        
        # place the cards on the stacks (initially, 13 on the crapette, 1 on each own tableau and rest in remainder)
        # self._cards_ui.place_stacks_cards_initially()
        
        # self._stacks_layout.render_collision_areas()
        # self._stacks_layout.render_tableau_cards_locations()
        
        # update the window
        pygame.display.flip()

    def check_for_collision(self, event: pygame.event.Event) -> str:
        
        area: str = "table" # default value: hit the table
        card_found: int = -1
        card_name_found: str = "none/table"
        
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
        
        
        #TODO: if there is no card on the stack, the collision should be with the table.
        # check the value of the card __str__ for this
        
        found_collision: bool = False
        for stack in collision_checklist_order:
            # card_rect, _ = self._ui_game_state.stacks_locations[stack]
            card_rect: pygame.Rect
            # for card_rect, card_num, card_name in reversed(self._ui_game_state.non_tableau_cards_positions[stack]):
            for card_rect, card_num, card_name in reversed(self._ui_game_state.cards_positions[stack]):
                if card_rect.collidepoint(event.pos):
                    if card_name != "":
                        area = stack
                        card_found = card_num
                        card_name_found = card_name
                        found_collision = True
        
        if not found_collision:
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
            # Check each tableau in order, from top-most card so we hit the top one first
            for tableau in tableau_checklist_order:
                if found_collision:
                    break

                # for card_rect, card_num, card_name in reversed(self._ui_game_state.tableau_cards_positions[tableau]):
                for card_rect, card_num, card_name in reversed(self._ui_game_state.cards_positions[tableau]):
                    if card_rect.collidepoint(event.pos):
                        if card_name != "":
                            area = tableau
                            found_collision = True
                            card_found = card_num
                            card_name_found = card_name
                            break
                    
        return f"Hit: {area=} {card_found=} {card_name_found=}"


