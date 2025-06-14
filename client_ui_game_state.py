import pygame
from pprint import pprint

from constants import CARD_IMG_WIDTH, CARD_IMG_HEIGHT, TABLEAU_CARDS_SHIFT,  TableColours
# ,GAME_WIDTH, GAME_HEIGHT

from game_logger import GameLogger, DebugLevel
client_logger: GameLogger = GameLogger("client_ui_game_state", level=DebugLevel.client_ui_game_state.value)


class UIGameState:
    
    _window: pygame.Surface  # the screen that contains the game
    _window_dimensions: tuple[int, int]
    _window_centre: tuple[int, int]
    _game_icon: pygame.Surface
    _table_colour: tuple[int, int, int]
    
    _originally_loaded_cards_faces: dict[str, pygame.Surface]  # the sprites from the original file
    _card_dimensions: tuple[int, int]  # (width, height)
    _cards_faces: dict[str, pygame.Surface]  # the scaled cards sprites [cardname: sprite]
    
    _tableau_stacks_cards_quantity: dict[str, int]
    _tableau_cards_shift: int  # the shift of the tableau card from the previous card of the same tableau stack
    _stacks_spacing_w: int  # the horizontal spacing between the stacks
    _stacks_spacing_y: int  # the vertical spacing between the stacks
    _stacks_positions: dict[str, tuple[pygame.Rect, bool]]  # (Stack location as rect, V(True)/H)
    
    _cards_positions: dict[str, list[tuple[pygame.Rect, int, str]]]  # location of cards. stackname(position-size, cardnum on the stack, cardname)
    
    # _non_tableau_cards_positions: dict[str, list[tuple[pygame.Rect, int, str]]]  # location of the non-tableau cards. non-tableaus, x, y
    # _tableau_cards_positions: dict[str, list[tuple[pygame.Rect, int, str]]]  # location of the tableau cards. tableaux, x, card__str__
    
    _is_moving: bool
    
    
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
        """The calculated location of the base of the stack on the game screen

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
        """Sets the stacks locations calculated for the current screen

        Args:
            stacks_locations (dict[str, tuple[int, int, bool]]): 
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
        
    def _set_stacks_locations(self) -> None:
        """
        Calculate the positions of the stacks
        Assign the top left corner coordiinate of the stacks
        Assign the orientation of the cards in the stacks           
        """
        
        # TODO: Rework these as rects, not (x,y)
        
        # x locations (top left corner)
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
        
        # y locations (top left corner)
        opponent_y = self.window_centre_y - self.card_height * 3 - int(self._stacks_spacing_y * 2.5)
        player_y = self.window_centre_y + self.card_height * 2 + int(self._stacks_spacing_y * 2.5)
        tableau_top_y = self.window_centre_y - self.card_height * 2 - int(self._stacks_spacing_y * 1.5)
        foundation_top_y = tableau_top_y + (self.card_height - self.card_width) //2
        tableau_spacing_y = self.card_height + self._stacks_spacing_y

        # Assign the locations
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
        
        center_stacks_positions: dict[str, tuple[pygame.Rect, bool]] = {}
        for p in range(4):
            o = 3 - p
            center_stacks_positions[f"opponent_tableau{p}"] = (pygame.Rect(opponent_tableau_x, tableau_top_y + tableau_spacing_y * o, self.card_width, self.card_height), True)
            center_stacks_positions[f"opponent_foundation{p}"] = (pygame.Rect(opponent_foundation_x, foundation_top_y + tableau_spacing_y * o, self.card_height, self.card_width), False)
            center_stacks_positions[f"player_tableau{p}"] = (pygame.Rect(player_tableau_x, tableau_top_y + tableau_spacing_y * p, self.card_width, self.card_height), True)
            center_stacks_positions[f"player_foundation{p}"] = (pygame.Rect(player_foundation_x, foundation_top_y + tableau_spacing_y * p, self.card_height, self.card_width), False)

        # combine the 3 dictionaries
        self._stacks_positions = opponent_base_stacks_positions |center_stacks_positions | player_base_stacks_positions    
    
    #endregion
    
    #region Cards Positions
    @property
    def cards_positions(self) -> dict[str, list[tuple[pygame.Rect, int, str]]]:
        """the ordered location of each card of the stack"""
        return self._cards_positions

    @cards_positions.setter
    def cards_positions(self, cards_positions: dict[str, list[tuple[pygame.Rect, int, str]]]) -> None:
        """Set the ordered location of each card of the stack"""
        self._cards_positions = cards_positions
    
    def _set_cards_positions(self) -> None:
        """Set the position of all the cards in all the stacks
        Values are set later when the information is available from the server"""
        
        # Step 1
        # Set the ordered position of each non-tableau card of the stack
        # All the cards are in the same position so needs to be handled differently from Tableau where a shift happens
        
        non_tableau_cards_stacks = [
            "player_crapette",
            "player_remainder",
            "player_bin",
            "player_foundation0",
            "player_foundation1",
            "player_foundation2",
            "player_foundation3",
            "opponent_crapette",
            "opponent_remainder",
            "opponent_bin",
            "opponent_foundation0",
            "opponent_foundation1",
            "opponent_foundation2",
            "opponent_foundation3",
        ]
        
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

        for stack in self.stacks_positions:
            # Initialise a rectangle at the base of the stack
            rect: pygame.Rect = self.stacks_positions[stack][0]

            if stack in non_tableau_cards_stacks:
                non_tableau_cards_positions[stack].append((rect , -1, ""))


        
        # Step 2:
        # Set the ordered position of each tableau card of the stack
        
        tableau_card_positions: dict[str, list[tuple[pygame.Rect, int, str]]] = {
            "player_tableau0":  [],
            "player_tableau1":  [],
            "player_tableau2":  [],
            "player_tableau3":  [],
            "opponent_tableau0": [],
            "opponent_tableau1": [],
            "opponent_tableau2": [],
            "opponent_tableau3": [],
        }
        
        for stack in self.stacks_positions:
            # Initialise a rectangle at the base of the stack
            rect = self.stacks_positions[stack][0]
            
            if "player_tableau" in stack:
                #12 should be sufficient in reality as the ace should 
                # go to the foundation, but...
                for card in range(13):
                    tableau_card_positions[stack].append((rect, card, ""))
                    rect = rect.move((self.tableau_cards_shift,0))
                    
            elif "opponent_tableau" in stack:
                #12 should be sufficient in reality as the ace should 
                # go to the foundation, but...
                for card in range(13):
                    tableau_card_positions[stack].append((rect, card, ""))
                    rect = rect.move((-self.tableau_cards_shift,0))
        
        
        # Step 3:
        # merge
        
        self._cards_positions = non_tableau_cards_positions | tableau_card_positions
        
        
    
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

    #region Card Shift
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
        self._set_stacks_locations()            # calculate and store the stacks base locations

        # self._set_tableau_cards_positions()
        # self._set_non_tableau_cards_positions()
        
        self._set_cards_positions()
        # pprint(f"{self.tableau_cards_positions}")
        # client_logger.debug(f"{self.tableau_cards_positions}")
        
        # client_logger.debug(f"{self.non_tableau_cards_positions}")
        