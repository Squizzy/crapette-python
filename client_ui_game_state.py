import pygame
from typing import TypedDict
from pprint import pprint

from constants import CARD_IMG_WIDTH, CARD_IMG_HEIGHT, TABLEAU_CARDS_SHIFT,  TableColours
# ,GAME_WIDTH, GAME_HEIGHT

from game_logger import GameLogger, DebugLevel
client_logger: GameLogger = GameLogger("client_ui_game_state", level=DebugLevel.client_ui_game_state.value)

# class CardToMove(TypedDict):
#        stack: str # stack found
#        card_name: str # card name found
#        card_pos_on_stack: int # card position on stack
#        card_rect_on_window: pygame.Rect # Position and size of the card found
#        card_sprite: pygame.Surface # the card sprite

class CardsPositions(TypedDict):
    stack: str  # stack found
    position: tuple[int, int]  # position of the card on the window (table)
    card_num: int  # card number on the stack
    card_name: str  # card name found
    card_rect_on_window: pygame.Rect  # Position and size of the card found
    card_sprite: pygame.Surface  # the card sprite

class CardToMove(TypedDict):
    stack: str
    card_name: str
    card_pos_on_stack: int
    card_rect_on_window: pygame.Rect
    # card_sprite: pygame.Surface 

# class MovingCard(TypedDict):
#     stack: str
#     card_name: str
#     card_pos_on_stack: int
#     card_rect_on_window:  pygame.Rect
    

class UIGameState:
    
    _window: pygame.Surface  # the screen that contains the game
    _window_dimensions: tuple[int, int]
    _window_centre: tuple[int, int]
    _game_icon: pygame.Surface
    _table_colour: tuple[int, int, int]
    
    _originally_loaded_cards_faces: dict[str, pygame.Surface]  # stores the sprites from the original file
    _card_dimensions: tuple[int, int]  # (width, height) - the dimensions recalculated for the window dimensions
    _cards_faces: dict[str, pygame.Surface]  # the cards sprites scaled for the window dimensions [cardname: sprite]
    
    _stacks_spacing_w: int  # the horizontal spacing between the stacks
    _stacks_spacing_y: int  # the vertical spacing between the stacks
    _stacks_positions: dict[str, tuple[pygame.Rect, bool]]  # stores the position of all the stacks for the window dimensions as (rect, V(True)/H)
    
    
    _tableau_stacks_cards_quantity: dict[str, int]  # TODO: REMOVE THIS EARLY DEV TEMP

    _tableau_cards_shift: int  # the shift of the tableau card from the previous tableau card of the same tableau
    _tableau_stack_card_slot_positions: dict[str, list[tuple[int, int]]]  # sotres the position of all the cards in the tableau stacks as (x, y) coordinates

    # _moving_cards: list[dict[str, str | int | pygame.Rect]] # (source) "stack", card_pos_on_stack", "card_rect_on_window", "card_name"
    _moving_cards: list[CardToMove]  # Contains all the cards that are currently attempted to be moved

    # TODO: as this is duplication information, it might be better to remove in time.
    _cards_positions: dict[str, list[tuple[pygame.Rect, int, str]]]  # location of all the cards on the window. as stackname: (position-size, cardnum on stack, cardname)

    
    # _non_tableau_cards_positions: dict[str, list[tuple[pygame.Rect, int, str]]]  # location of the non-tableau cards. non-tableaus, x, y
    # _tableau_cards_positions: dict[str, list[tuple[pygame.Rect, int, str]]]  # location of the tableau cards. tableaux, x, card__str__
    
    _is_moving: bool  # value set if a card has been selected (mousedown) to be moved to another stack
    _card_to_move: CardToMove  # The card that has been selected to be moved to another stack
    # _card_to_move: dict[str, str | int | pygame.Rect | pygame.Surface]
    # _card_to_move: dict[str, str| int| pygame.Rect | pygame.Surface]
    # _card_to_move: dict
    # _card_to_move_sprite: pygame.Surface
    # _card_to_move_rect: pygame.Rect

    
    def __init__(self) -> None:
        self._card_dimensions = (0, 0)
        self._originally_loaded_cards_faces = {}
        self._cards_faces = {}

        self._tableau_stacks_cards_quantity = {
            "player_tableau0": 1,
            "player_tableau1": 1,
            "player_tableau2": 1,
            "player_tableau3": 1,
            "opponent_tableau0": 5,
            "opponent_tableau1": 1,
            "opponent_tableau2": 1,
            "opponent_tableau3": 1,
        }
        self._stacks_positions = {}
        # self._tableau_cards_positions = {}
        # self._non_tableau_cards_positions = {}
        
        self.table_colour = TableColours.FELT_GREEN
        self._is_moving = False
        self._moving_cards = []
        self.reset_card_to_move()
        # self._click_pos = (int, int)
     
    #region window: the game area not including the title bar
    @property
    def window(self) -> pygame.Surface:
        return self._window
    
    @window.setter
    def window(self, surface: pygame.Surface) -> None:
        """assign the window surface"""
        self._window = surface
    
    @property
    def window_dimensions(self) -> tuple[int, int]:
        """The dimensions of the game screen"""
        # if not self._window_dimensions:
        #     rect = self.window.get_rect()
        #     self.window_dimensions = rect.w, rect.h
        return self._window_dimensions
    
    def _set_window_dimensions(self) -> None:
        """set the window_dimensions variable using the window dimensions"""
        rect = self.window.get_rect()
        self._window_dimensions = rect.w, rect.h
    
    @property
    def window_width(self) -> int:
        """The width of the game screen"""
        return self._window_dimensions[0]
    
    @property
    def window_height(self) -> int:
        """The width of the game screen"""
        return self._window_dimensions[1]
    
    @property 
    def window_centre(self) -> tuple[int, int]:
        """The centre of the game screen"""
        return self._window_centre
    
    def _set_window_centre(self) -> None:
        rect = self.window.get_rect()
        self._window_centre = rect.w // 2, rect.h // 2
    
    @property 
    def window_centre_x(self) -> int:
        """returns the x  position of the centre point"""
        return self.window_centre[0]
    
    @property
    def window_centre_y(self) -> int:
        """returns the y position of the centre point"""
        return self._window_centre[1]
    
    #endregion
    
    #region table colour
    @property
    def table_colour(self) -> tuple[int, int, int]:
        """return the colour used for the background of the game"""
        return self._table_colour
    
    @table_colour.setter
    def table_colour(self, table_colour: tuple[int, int, int]) -> None:
        """sets the background colour for the game"""
        self._table_colour = table_colour

    #endregion

    #region game icon
    @property
    def game_icon(self) -> pygame.Surface:
        """The game icon used in the game window"""
        return self._game_icon
    
    @game_icon.setter
    def game_icon(self, game_icon: pygame.Surface) -> None:
        """sets the game icon for the game window"""
        self._game_icon = game_icon
    
    #endregion
    
    #region Cards
    @property
    def card_dimensions(self) -> tuple[int, int]:
        """Dimensions of the card for the size of the window

        Returns:
            tuple[int, int]: width, height
        """
        # if self._card_dimensions == (0, 0):
        #     self.scale_card_dimensions()
        return self._card_dimensions

    @card_dimensions.setter
    def card_dimensions(self, dimensions: tuple[int, int]) -> None:
    # def card_dimensions(self, dimensions: tuple[int, int] | None) -> tuple[int, int]:
        """Set the scaled card dimensions"""
        # if dimensions is None:
        #     self.scale_card_dimensions()
        # else:
        self._card_dimensions = dimensions
        # return self._card_dimensions

    @property
    def card_width(self) -> int:
        """The width of the card (vertical) proportional to the window size"""
        return self._card_dimensions[0]
    
    @property
    def card_height(self) -> int:
        """The height of the card (horizontal) proportional to the window size"""
        return self._card_dimensions[1]

    def _set_card_dimensions(self) -> None:
        """set the card dimensions for the window size"""
        h: int = self.window_height // 7
        w: int = h * CARD_IMG_WIDTH // CARD_IMG_HEIGHT
        
        self._card_dimensions = (w, h)

    #endregion
   
    #region Card faces
    @property
    def originally_loaded_cards_faces(self) -> dict[str, pygame.Surface]:
        """returns all the cards sprites as loaded from the image files"""
        return self._originally_loaded_cards_faces
    
    @originally_loaded_cards_faces.setter
    def originally_loaded_cards_faces(self, faces: dict[str, pygame.Surface]) -> None:
        """Set the original loaded cards faces, then generate the scaled cards faces"""
        # load the original cards
        self._originally_loaded_cards_faces = faces
        
        # immediately resize the sprites to be used
        self._scale_cards_faces()
    
    def _scale_cards_faces(self) -> None:
        """Generate the scaled cards faces from the original loaded cards faces"""
        for card_face in self._originally_loaded_cards_faces:
            self._cards_faces[card_face] = pygame.transform.smoothscale( \
                                        self._originally_loaded_cards_faces[card_face],
                                        self.card_dimensions) 
        
    @property
    def cards_faces(self) -> dict[str, pygame.Surface]:
        """returns all the cards faces"""
        return self._cards_faces

    def card_face(self, card_name: str) -> pygame.Surface:
        """Returns the card sprite for the given card name"""
        return self._cards_faces[card_name]

    #endregion

    #region Stacks
    @property
    def stacks_positions(self) -> dict[str, tuple[pygame.Rect, bool]]:
        """The calculated position of the base of the stack on the game screen

        Returns:
            dict[str, tuple[int, int, bool]]: 
                dictionary of:
                    stack name: 
                        top left corner x offset, 
                        top left corner y offset, 
                        Vertical layout of the stack (True) or Horizontal layout    
        """
        return self._stacks_positions
    
    @stacks_positions.setter
    def stacks_positions(self, stacks_positions: dict[str, tuple[pygame.Rect, bool]]) -> None:
        """Sets the stacks positions calculated for the current screen

        Args:
            stacks_positions (dict[str, tuple[int, int, bool]]): 
                dictionary of:
                    stack name: 
                        top left corner x offset, 
                        top left corner y offset, 
                        Vertical layout of the stack (True) or Horizontal layout  
        """
        self._stacks_positions = stacks_positions
        # self._set_collision_areas()

    def _set_stacks_spacing(self) -> None:
        """Set the spacing between the stacks"""
        
        self._stacks_spacing_w = self.card_width // 7
        self._stacks_spacing_y = self.card_height // 7
        
    def _set_stacks_positions(self) -> None:
        """ Sets the position for all the card stacks on the window
            Assign the top left corner coordinate of the stacks
                For the Tableau stacks, the coordinate only represents the 
                position of the first (bottom of pile) card, as the next ones are shifted
            Assign the orientation of the cards in the stacks
        """

        # 1. Calculate x and y for each stack
        # x positions (top left corner)
        player_center_x = self.window_centre_x - self.card_width // 2
        player_left_x = player_center_x - self.card_width - self._stacks_spacing_w
        player_right_x = player_center_x + self.card_width + self._stacks_spacing_w
        player_foundation_x = self.window_centre_x + self._stacks_spacing_w
        player_tableau_x = player_foundation_x + self._stacks_spacing_w + self.card_height
         
        opponent_center_x = self.window_centre_x - self.card_width // 2
        opponent_left_x = opponent_center_x - self.card_width - self._stacks_spacing_w
        opponent_right_x = opponent_center_x + self.card_width + self._stacks_spacing_w
        opponent_foundation_x = self.window_centre_x - self._stacks_spacing_w - self.card_height
        opponent_tableau_x = opponent_foundation_x - self._stacks_spacing_w - self.card_width
        
        # y positions (top left corner)
        opponent_y = self.window_centre_y - self.card_height * 3 - int(self._stacks_spacing_y * 2.5)
        player_y = self.window_centre_y + self.card_height * 2 + int(self._stacks_spacing_y * 2.5)
        tableau_top_y = self.window_centre_y - self.card_height * 2 - int(self._stacks_spacing_y * 1.5)
        foundation_top_y = tableau_top_y + (self.card_height - self.card_width) //2
        tableau_spacing_y = self.card_height + self._stacks_spacing_y

        # 2. Assign the positions
        opponent_base_stacks_positions: dict[str, tuple[pygame.Rect, bool]] = {
            "opponent_crapette":    (pygame.Rect(opponent_right_x,  opponent_y, self.card_width, self.card_height), True),
            "opponent_remainder":   (pygame.Rect(opponent_center_x, opponent_y, self.card_width, self.card_height), True),
            "opponent_bin":         (pygame.Rect(opponent_left_x, opponent_y, self.card_width, self.card_height), True),
        }

        player_base_stacks_positions: dict[str, tuple[pygame.Rect, bool]] = {
            "player_crapette":  (pygame.Rect(player_left_x, player_y, self.card_width, self.card_height), True),
            "player_remainder": (pygame.Rect(player_center_x, player_y, self.card_width, self.card_height), True),
            "player_bin":       (pygame.Rect(player_right_x, player_y, self.card_width, self.card_height), True),
        }
        
        tableau_stacks_positions: dict[str, tuple[pygame.Rect, bool]] = {}
        for p in range(4):
            o = 3 - p
            tableau_stacks_positions[f"opponent_tableau{p}"] = (pygame.Rect(opponent_tableau_x, tableau_top_y + tableau_spacing_y * o, self.card_width, self.card_height), True)
            tableau_stacks_positions[f"player_tableau{p}"] = (pygame.Rect(player_tableau_x, tableau_top_y + tableau_spacing_y * p, self.card_width, self.card_height), True)
            
        foundation_stacks_positions: dict[str, tuple[pygame.Rect, bool]] = {}
        for p in range(4):
            o = 3 - p
            tableau_stacks_positions[f"opponent_foundation{p}"] = (pygame.Rect(opponent_foundation_x, foundation_top_y + tableau_spacing_y * o, self.card_height, self.card_width), False)
            tableau_stacks_positions[f"player_foundation{p}"] = (pygame.Rect(player_foundation_x, foundation_top_y + tableau_spacing_y * p, self.card_height, self.card_width), False)

        # 3. combine the 3 dictionaries and store
        self._stacks_positions = opponent_base_stacks_positions | tableau_stacks_positions | foundation_stacks_positions | player_base_stacks_positions    
    
        # 4. ensure the tableau card slot positions are calculated
        self._set_tableau_cards_slot_position()

    def _set_tableau_cards_slot_position(self) -> None:
        """ Sets the position for each of the 13 cards of each tableau on the window
            Method called by _set_stacks_positions method as it depends on 
            calculations of coordinates of stacks positions
        """

        self._tableau_stack_card_slot_positions = {
            "player_tableau0": [],
            "player_tableau1": [],
            "player_tableau2": [],
            "player_tableau3": [],
            "opponent_tableau0": [],
            "opponent_tableau1": [],
            "opponent_tableau2": [],
            "opponent_tableau3": [],
        }

        for stack in self.stacks_positions:
            if "tableau" in stack:
                for card_num in range(13):
                    x: int
                    y: int
                    if "player" in stack:
                        x = self.stacks_positions[stack][0].x + card_num * self.tableau_cards_shift
                    else:
                        x = self.stacks_positions[stack][0].x - card_num * self.tableau_cards_shift
                    y = self.stacks_positions[stack][0].y
                    self._tableau_stack_card_slot_positions[stack].append((x, y))
                    
        # client_logger.debug(f"{self._tableau_stack_card_slot_positions}")
                    

    def get_stack_position(self, stack: str) -> tuple[int, int]:
        """returns the (x, y) coordinate of a given non-tableau stack

        Args:
            stack (str): stack to place the card on

        Returns:
            tuple[int, int]: the coordinate of the card on the window (table)
        """
        return self._stacks_positions[stack][0].x, self._stacks_positions[stack][0].y

    def is_stack_vertical(self, stack) -> bool:
        """ informs if the stack is to be placed vertically or horizontally

        Returns:
            true if the card is supposed to be placed vertical (portrait)
        """
        # TODO: ought to be tightened to make sure the stack is an existing stack name
        for key, stack_position in self._stacks_positions.items():
            if not stack_position[1]:
                return False
        return True

    def get_tableau_card_slot_position(self, stack: str, card_num: int) -> tuple[int, int]:
        """returns the (x, y) coordinate of a card for a given tableau stack

        Args:
            stack (str): stack to place the card on
            card_num (int): card position in the stack

        Returns:
            tuple[int, int]: the coordinate of the card on the window (table)
        """
        return self._tableau_stack_card_slot_positions[stack][card_num]

    #endregion
    
    #region Cards Positions
    @property
    def cards_positions(self) -> dict[str, list[tuple[pygame.Rect, int, str]]]:
        """the ordered position of each card of the stack"""
        return self._cards_positions

    @cards_positions.setter
    def cards_positions(self, cards_positions: dict[str, list[tuple[pygame.Rect, int, str]]]) -> None:
        """Set the ordered position of each card of the stack"""
        self._cards_positions = cards_positions
    
    def _initialise_cards_positions(self) -> None:
        """ Initialise the _cards_positions dictionary
        Set the position of all the cards in all the stacks
        Values are set later when the information is available from the server
        """
        
        # Step 1
        # Set the ordered position of each non-tableau card of the stack
        # All the cards are in the same position so needs to be handled differently from Tableau where a shift happens
        
        non_tableau_cards_positions: dict[str, list[tuple[pygame.Rect, int, str]]] = {
            "player_crapette": [],
            "player_remainder": [],
            "player_bin": [],
            "player_foundation0":  [],
            "player_foundation1":  [],
            "player_foundation2":  [],
            "player_foundation3":  [],
            "opponent_crapette": [],
            "opponent_remainder": [],
            "opponent_bin": [],
            "opponent_foundation0": [],
            "opponent_foundation1": [],
            "opponent_foundation2": [],
            "opponent_foundation3": [],
        }

        tableau_cards_positions: dict[str, list[tuple[pygame.Rect, int, str]]] = {
            "player_tableau0":  [],
            "player_tableau1":  [],
            "player_tableau2":  [],
            "player_tableau3":  [],
            "opponent_tableau0": [],
            "opponent_tableau1": [],
            "opponent_tableau2": [],
            "opponent_tableau3": [],
        }
        
        moving_cards_positions:  dict[str, list[tuple[pygame.Rect, int, str]]] = {
            "moving_cards": [],
        }


        # Trying to move this here in case I don't need the below
        self._cards_positions = non_tableau_cards_positions | tableau_cards_positions | moving_cards_positions




        # non_tableau_cards_stacks = [
        #     "player_crapette",
        #     "player_remainder",
        #     "player_bin",
        #     "player_foundation0",
        #     "player_foundation1",
        #     "player_foundation2",
        #     "player_foundation3",
        #     "opponent_crapette",
        #     "opponent_remainder",
        #     "opponent_bin",
        #     "opponent_foundation0",
        #     "opponent_foundation1",
        #     "opponent_foundation2",
        #     "opponent_foundation3",
        # ]
        
        
        # for stack in self.stacks_positions:
        #     # Initialise a rectangle at the base of the stack
        #     rect: pygame.Rect = self.stacks_positions[stack][0]

        #     if stack in non_tableau_cards_stacks:
        #         # Foundations will have 13 cards max, you never know, 
        #         # the ace might be put there then has to be moved at the right time not to cause a crapette.
        #         if "foundation" in stack:
        #             for card_num in range(13):
        #                 non_tableau_cards_positions[stack].append((rect , card_num, ""))
                
        #         # In extreme case (impossible) other player stacks will have 104 cards (2x decks of cards)
        #         else:
        #             for card_num in range(104):
        #                 non_tableau_cards_positions[stack].append((rect , card_num, ""))
        
        # # 13 cards should never be moved, but you never know, as long as the ace is moved asap...
        # for card_num in range(13):
        #     moving_cards_positions["moving_cards"].append((rect, card_num, ""))
        
        # # Step 2:
        # # Set the ordered position of each tableau card of the stack
        
        # for stack in self.stacks_positions:
        #     # Initialise a rectangle at the base of the stack
        #     rect = self.stacks_positions[stack][0]
            
        #     if "player_tableau" in stack:
        #         #12 should be sufficient in reality as the ace should 
        #         # go to the foundation, but...
        #         for card_num in range(13):
        #             tableau_cards_positions[stack].append((rect, card_num, ""))
        #             rect = rect.move((self.tableau_cards_shift, 0))
                    
        #     elif "opponent_tableau" in stack:
        #         #12 should be sufficient in reality as the ace should 
        #         # go to the foundation, but...
        #         for card_num in range(13):
        #             tableau_cards_positions[stack].append((rect, card_num, ""))
        #             rect = rect.move((-self.tableau_cards_shift, 0))
        
        
        # # Step 3:
        # # merge
        
        # self._cards_positions = non_tableau_cards_positions | tableau_cards_positions
        # # pprint(f"{non_tableau_cards_positions}")
        # # pprint(f"{tableau_cards_positions}")
        # # input()
        
    def set_card_in_positions(self) -> None:
        ...


    #region Moving Cards
    @property
    def moving_cards(self) -> list[CardToMove]:
    # def moving_cards(self) -> list[tuple[str, int, pygame.Rect, str]]:
        """Returns the list of moving cards

        returns:
            list[dict [str | int | pygame.Rect]
                (source) "stack", 
                "card_pos_on_stack", 
                "card_rect_on_window", 
                "card_name"
        """
        return self._moving_cards

    @moving_cards.setter
    def moving_cards(self, moving_cards: list[CardToMove]) -> None:
    # def moving_cards(self, moving_cards: list[tuple[str, int, pygame.Rect, str]]) -> None:
        """Sets the moving cards
        
        Args:
            list[dict [str | int | pygame.Rect]
                (source) "stack", 
                "card_pos_on_stack", 
                "card_rect_on_window", 
                "card_name"
        """
        # for card in moving_cards:
        self._moving_cards = moving_cards
        
        

    def reset_moving_cards(self) -> None:
        """Resets the moving cards list"""
        self.moving_cards = []


            

    # @property
    # def tableau_cards_positions(self) -> dict[str, list[tuple[pygame.Rect, int, str]]]:
    #     """the ordered location of each card of the stack"""
    #     return self._tableau_cards_positions
    
    # @tableau_cards_positions.setter
    # def tableau_cards_positions(self, tableau_cards_locations: dict[str, list[tuple[pygame.Rect, int, str]]]) -> None:
    #     """Set the ordered location of each card of the stack"""
    #     self._tableau_cards_positions = tableau_cards_locations
    
    # def _set_tableau_cards_positions(self) -> None:
        
    #     tableau_card_positions: dict[str, list[tuple[pygame.Rect, int, str]]] = {
    #         "player_tableau0":  [],
    #         "player_tableau1":  [],
    #         "player_tableau2":  [],
    #         "player_tableau3":  [],
    #         "opponent_tableau0": [],
    #         "opponent_tableau1": [],
    #         "opponent_tableau2": [],
    #         "opponent_tableau3": [],
    #     }
        
    #     for stack in self.stacks_positions:
    #         # Initialise a rectangle at the base of the stack
    #         rect:pygame.Rect = self.stacks_positions[stack][0]
            
    #         if "player_tableau" in stack:
    #             #TODO: 12 should be sufficient in reality as the ace should 
    #             # go to the foundation, but...
    #             for card in range(13):
    #                 tableau_card_positions[stack].append((rect, card, ""))
    #                 rect = rect.move((self.tableau_cards_shift,0))
                    
    #         elif "opponent_tableau" in stack:
    #             #TODO: 12 should be sufficient in reality as the ace should 
    #             # go to the foundation, but...
    #             for card in range(13):
    #                 tableau_card_positions[stack].append((rect, card, ""))
    #                 rect = rect.move((-self.tableau_cards_shift,0))
        
    #     self._tableau_cards_positions = tableau_card_positions.copy()
        
    # @property
    # def non_tableau_cards_positions(self) -> dict[str, list[tuple[pygame.Rect, int, str]]]:
    #     """the ordered location of each non-tableau card of the stack"""
    #     return self._non_tableau_cards_positions
    
    # @non_tableau_cards_positions.setter
    # def non_tableau_cards_positions(self, non_tableau_cards_locations: dict[str, list[tuple[pygame.Rect, int, str]]]) -> None:
    #     """Set the ordered location of each non-tableau card of the stack"""
    #     self._non_tableau_cards_positions = non_tableau_cards_locations
        
    # def _set_non_tableau_cards_positions(self) -> None:
    #     """Set the ordered location of each non-tableau card of the stack"""
        
    #     non_tableau_cards_stacks = [
    #         "player_crapette",
    #         "player_remainder",
    #         "player_bin",
    #         "player_foundation0",
    #         "player_foundation1",
    #         "player_foundation2",
    #         "player_foundation3",
    #         "opponent_crapette",
    #         "opponent_remainder",
    #         "opponent_bin",
    #         "opponent_foundation0",
    #         "opponent_foundation1",
    #         "opponent_foundation2",
    #         "opponent_foundation3",
    #     ]
        
    #     non_tableau_cards_positions: dict[str, list[tuple[pygame.Rect, int, str]]] = {
    #         "player_crapette": [],
    #         "player_remainder": [],
    #         "player_bin": [],
    #         "player_foundation0":  [],
    #         "player_foundation1":  [],
    #         "player_foundation2":  [],
    #         "player_foundation3":  [],
    #         "opponent_crapette": [],
    #         "opponent_remainder": [],
    #         "opponent_bin": [],
    #         "opponent_foundation0": [],
    #         "opponent_foundation1": [],
    #         "opponent_foundation2": [],
    #         "opponent_foundation3": [],
    #     }

    #     for stack in self.stacks_positions:
    #         # Initialise a rectangle at the base of the stack
    #         rect: pygame.Rect
    #         rect = self.stacks_positions[stack][0]

    #         if stack in non_tableau_cards_stacks:
    #             non_tableau_cards_positions[stack].append((rect , -1, ""))

    #     self.non_tableau_cards_positions = non_tableau_cards_positions.copy()

    #endregion

    #region Tableau Card Shift
    @property
    def tableau_cards_shift(self) -> int:
        """The shift of the tableau card from the previous card of the same tableau stack

        Returns:
            int: the shift in pixels
        """
        # self._set_tableau_cards_shift()
        return self._tableau_cards_shift
    
    @tableau_cards_shift.setter
    def tableau_cards_shift(self, new_shift: int | None) -> None:
        """set the tableau card shift value"""
        if new_shift is None:
            self._set_tableau_cards_shift()
        else:
            self._tableau_cards_shift = new_shift
    
    def _set_tableau_cards_shift(self) -> None:
        """Calculate the shift of the tableau cards from the previous card of the same tableau stack"""
        self._tableau_cards_shift = self.card_width // TABLEAU_CARDS_SHIFT

    #endregion
    
    #region Card To Move
    @property
    def card_to_move(self) -> CardToMove:
    # def card_to_move(self) -> dict[str, str| int| pygame.Rect | pygame.Surface]:
        """the card to be moved"""
        return self._card_to_move
    
    @card_to_move.setter
    def card_to_move(self, card_to_move: CardToMove) -> None:
    # def card_to_move(self, card_to_move: dict[str, str| int| pygame.Rect | pygame.Surface]) -> None:
        """Set the card to be moved"""
        self._card_to_move = card_to_move
    
    def reset_card_to_move(self) -> None:
        self._card_to_move = CardToMove(
            stack = "", # stack found
            card_name = "", # card name found
            card_pos_on_stack = -1, # card position on stack
            card_rect_on_window = pygame.Rect((0,0,0,0)) # Position and size of the card found
            # "card_sprite": pygame.Surface((1,1)
            )
            
    
    #endregion

    # Events Handling
    def on_window_resize(self, surface: pygame.Surface):

        self._window = surface
        
        self._set_window_dimensions()          # Store the window dimensions (w, h)
        self._set_window_centre()              # Store the window centre (x, y)
        
        self._set_card_dimensions()             # Store the scaled cards sprite dimensions for the window size (w, h)
        self._scale_cards_faces()
        
        # below two need to be set before the stacks location is set
        # as the collision area is calculated immediate when the stacks location is set
        # and it needs these values

        self._set_tableau_cards_shift()        # Store the shift of the tableau card from the previous card of the same tableau stack
        self._set_stacks_spacing()              # Calculate and store the stacks spacings
        self._set_stacks_positions()            # calculate and store the stacks base locations

        # self._set_tableau_cards_positions()
        # self._set_non_tableau_cards_positions()
        
        self._initialise_cards_positions()
        # pprint(f"{self.tableau_cards_positions}")
        # client_logger.debug(f"{self.tableau_cards_positions}")
        
        # client_logger.debug(f"{self.non_tableau_cards_positions}")
        