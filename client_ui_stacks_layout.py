import pygame

from constants import GAME_HEIGHT, GAME_WIDTH
from client_ui_cards import CardsUI   
from client_ui_game_state import UIGameState
from game_logger import GameLogger

client_logger: GameLogger

class StacksLayoutUI:
    _ui_game_state: UIGameState
    _screen_width: int
    _screen_height: int
    _center_x: int
    _center_y: int
    _margin_x: int
    _margin_y: int
    _cards:  CardsUI
    # _locations: dict[str, tuple[int, int, bool]]
    
    def __init__(self, logger: GameLogger, cards: CardsUI, ui_game_state: UIGameState) -> None:
        """
        Initialise the stacks layout
        Calculate the positions of the stacks
        Store the positions in the _positions attribute
        """
        global client_logger
        client_logger = logger
        
        self._ui_game_state = ui_game_state
        
        # Initiate the screen dimensions
        self._screen_width = GAME_WIDTH
        self._screen_height = GAME_HEIGHT
        self._center_x = self._screen_width // 2
        self._center_y = self._screen_height // 2
        
        # Get the cards graphics
        self._cards = cards
        # Initiate the margin between the stacks
        self._margin_x = self._ui_game_state.card_dimensions[0] // 7
        self._margin_y = self._ui_game_state.card_dimensions[1] // 7
        # self._margin_x = self._cards.width // 7
        # self._margin_y = self._cards.height // 7
        
        # Calculate the positions of the stacks for the screen dimensions
        # self._locations = self._calculate_locations()
        self._ui_game_state.stacks_locations = self._calculate_locations()
        
    # @property
    # def stacks_locations(self) -> dict[str, tuple[int, int, bool]]:
    #     """ 
    #     Get the locations of the stacks
        
    #     Returns:
    #         dict[str, tuple[int, int, bool]]: a dictionary containing:
    #             - key: the name of the stack
    #             - values:
    #                 - the top left corner coordinate of the bottom of the stack x, y
    #                 - a boolean indicating if the card is placed vertically or horizontally
    #     """
    #     return self._game_ui_state._stacks_locations
    
    # def set_screen_dimensions(self, screen_width: int, screen_height: int) -> None:
    #     self._screen_width = screen_width
    #     self._screen_height = screen_height
        
    def _calculate_locations(self) -> dict[str, tuple[int, int, bool]]:
        """
        Calculate the positions of the stacks
        Assign the top left corner coordiinate of the stacks
        Assign the orientation of the cards in the stacks

        Returns:
            dict[str, tuple[int, int, bool]]: a dictionary containing:
                - the name of the stack
                - the top left corner coordinate of the bottom of the stack
                - a boolean indicating if the card is placed vertically or horizontally
            
        """
        
        # self._cards.width = self._ui_game_state.card_dimensions[0]
        # self._cards.height = self._ui_game_state.card_dimensions[1]
        
        
        
        
        
        # x positions (top left corner)
        player_center_x = self._center_x - self._ui_game_state.card_dimensions[0] // 2
        player_left_x = player_center_x - self._ui_game_state.card_dimensions[0] - self._margin_x
        player_right_x = player_center_x + self._ui_game_state.card_dimensions[0] + self._margin_x
        player_foundation_x = self._center_x + self._margin_x
        player_tableau_x = player_foundation_x + self._margin_x + self._ui_game_state.card_dimensions[1]
        # player_center_x = self._center_x - self._cards.width // 2
        # player_left_x = player_center_x - self._cards.width - self._margin_x
        # player_right_x = player_center_x + self._cards.width + self._margin_x
        # player_foundation_x = self._center_x + self._margin_x
        # player_tableau_x = player_foundation_x + self._margin_x + self._cards.height
        
        opponent_center_x = self._center_x - self._ui_game_state.card_dimensions[0] // 2
        opponent_left_x = opponent_center_x - self._ui_game_state.card_dimensions[0] - self._margin_x
        opponent_right_x = opponent_center_x + self._ui_game_state.card_dimensions[0] + self._margin_x
        opponent_foundation_x = self._center_x - self._margin_x - self._ui_game_state.card_dimensions[1]
        opponent_tableau_x = opponent_foundation_x - self._margin_x - self._ui_game_state.card_dimensions[0]
        # opponent_center_x = self._center_x - self._cards.width // 2
        # opponent_left_x = opponent_center_x - self._cards.width - self._margin_x
        # opponent_right_x = opponent_center_x + self._cards.width + self._margin_x
        # opponent_foundation_x = self._center_x - self._margin_x - self._cards.height
        # opponent_tableau_x = opponent_foundation_x - self._margin_x - self._cards.width
        
        # y positions (top left corner)
        opponent_y = self._center_y - self._ui_game_state.card_dimensions[1] * 3 - int(self._margin_y * 2.5)
        player_y = self._center_y + self._ui_game_state.card_dimensions[1] * 2 + int(self._margin_y * 2.5)
        tableau_top_y = self._center_y - self._ui_game_state.card_dimensions[1] * 2 - int(self._margin_y * 1.5)
        foundation_top_y = tableau_top_y + (self._ui_game_state.card_dimensions[1] - self._ui_game_state.card_dimensions[0]) //2
        tableau_spacing_y = self._ui_game_state.card_dimensions[1] + self._margin_y
        # opponent_y = self._center_y - self._cards.height * 3 - int(self._margin_y * 2.5)
        # player_y = self._center_y + self._cards.height * 2 + int(self._margin_y * 2.5)
        # tableau_top_y = self._center_y - self._cards.height * 2 - int(self._margin_y * 1.5)
        # foundation_top_y = tableau_top_y + (self._cards.height - self._cards.width) //2
        # tableau_spacing_y = self._cards.height + self._margin_y
        # foundation_spacing_y = tableau_spacing_y + self._margin_y
        
        opponent_base_stacks_positions: dict[str, tuple[int, int, bool]] = {
            "opponent_crapette":    (opponent_right_x,  opponent_y, True),
            "opponent_remainder":   (opponent_center_x, opponent_y, True),
            "opponent_bin":         (opponent_left_x, opponent_y, True),
        }

        player_base_stacks_positions: dict[str, tuple[int, int, bool]] = {
            "player_crapette":  (player_left_x, player_y, True),
            "player_remainder": (player_center_x, player_y, True),
            "player_bin":       (player_right_x, player_y, True),
        }
        
        center_stacks_positions: dict[str, tuple[int, int, bool]] = {}
        for p in range(4):
            o = 3 - p
            center_stacks_positions[f"opponent_tableau{p}"] = (opponent_tableau_x, tableau_top_y + tableau_spacing_y * o, True)
            center_stacks_positions[f"opponent_foundation{p}"] = (opponent_foundation_x, foundation_top_y + tableau_spacing_y * o, False)
            center_stacks_positions[f"player_tableau{p}"] = (player_tableau_x, tableau_top_y + tableau_spacing_y * p, True)
            center_stacks_positions[f"player_foundation{p}"] = (player_foundation_x, foundation_top_y + tableau_spacing_y * p, False)

    #             f"opponent_tableau_4":   (opponent_tableau_x, tableau_top_y, True),
    #             f"opponent_tableau_3":   (opponent_tableau_x, tableau_top_y + tableau_spacing_y, True),
    #             f"opponent_tableau_2":   (opponent_tableau_x, tableau_top_y + tableau_spacing_y * 2, True),
    #             f"opponent_tableau_1":   (opponent_tableau_x, tableau_top_y + tableau_spacing_y * 3, True),
    #             f
    #             f"opponent_foundation_4": (opponent_foundation_x, foundation_top_y, False),
    #             f"opponent_foundation_3": (opponent_foundation_x, foundation_top_y + foundation_spacing_y, False),
    #             f"opponent_foundation_2": (opponent_foundation_x, foundation_top_y + foundation_spacing_y * 2, False),
    #             f"opponent_foundation_1": (opponent_foundation_x, foundation_top_y + foundation_spacing_y * 3, False),
    # f
    #             f"player_foundation_1": (player_foundation_x, foundation_top_y, False),
    #             f"player_foundation_2": (player_foundation_x, foundation_top_y + foundation_spacing_y, False),
    #             f"player_foundation_3": (player_foundation_x, foundation_top_y + foundation_spacing_y * 2, False),
    #             f"player_foundation_4": (player_foundation_x, foundation_top_y + foundation_spacing_y * 3, False),
    # f
    #             f"player_tableau_1": (player_tableau_x, tableau_top_y, True),
    #             f"player_tableau_2": (player_tableau_x, tableau_top_y + tableau_spacing_y, True),
    #             f"player_tableau_3": (player_tableau_x, tableau_top_y + tableau_spacing_y * 2, True),
    #             f"player_tableau_4": (player_tableau_x, tableau_top_y + tableau_spacing_y * 3, True),

        # }
        # combine the 3 dictionaries
        stacks_locations = opponent_base_stacks_positions |center_stacks_positions | player_base_stacks_positions    
        return stacks_locations
    
    def update_stacks_locations_and_sizes(self, width: int, height: int, cards: CardsUI) -> None:
        """
        Resize the screen
        Recalculate the positions of the stacks
        
        Args:
            width, height (int): new dimensions of the screen
            cards (Cards): the set of card graphics to use
        """
        # update the screen dimensions
        self._screen_width = width
        self._screen_height = height
        self._center_x = self._screen_width // 2
        self._center_y = self._screen_height // 2
        
        # update the card dimensions
        self._cards = cards
        # self._cards.scale_cards_faces()
        self._ui_game_state.scale_cards_faces()

        # update the margin between the stacks
        self._margin_x = self._ui_game_state.card_dimensions[0] // 7
        self._margin_y = self._ui_game_state.card_dimensions[1] // 7
        # self._margin_x = self._cards.width // 7
        # self._margin_y = self._cards.height // 7
        
        # calculate the positions of the stacks
        self._ui_game_state.stacks_locations = self._calculate_locations()
        # self._locations = self._calculate_locations()

    def render_empty_stacks(self, surface: pygame.Surface, cards: CardsUI):
        """
        Display the stacks positions using an empty card. 

        Args:
            surface (pygame.Surface): The surface to display on
            cards (Cards): the set of card graphics to use
        """
        stacks_locations = self._ui_game_state._stacks_locations
        
        card_face: str = "EC"
        # card_face = "HQ"
        
        # tcards: list[str] = []
        # for card, _ in self._ui_game_state._cards_faces.items():
        #     tcards.append(card)
        
        # client_logger.debug(f"{tcards=}")
        # client_logger.debug(f"{self._ui_game_state._cards_faces=}")
        
        # card_graphics = self._ui_game_state._cards_faces[card_face]
        card_graphics = self._ui_game_state.card_face(card_face)

        for stack in stacks_locations:
            (x, y, vertical) = stacks_locations[stack]
            blank_blit = card_graphics if vertical else pygame.transform.rotate(card_graphics.copy(), 90)
            # bw: int = blank_blit.get_width()
            # bh: int = blank_blit.get_height()
            # print(f"{bw=} {bh=}")
            if card_face == "EC":
                blank_blit.set_colorkey(blank_blit.get_at((3,3)))
            
            surface.blit(blank_blit, (x, y) )
