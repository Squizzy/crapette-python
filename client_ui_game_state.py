import pygame
from constants import CARD_IMG_WIDTH, CARD_IMG_HEIGHT, GAME_WIDTH, GAME_HEIGHT

class UIGameState:
    _surface: pygame.Surface  # the screen that contains the game
    _screen_dimensions: tuple[int,  int]  # (width, height) 
    _card_dimensions: tuple[int, int]  # (width, height)
    _originally_loaded_cards_faces: dict[str, pygame.Surface]  # the sprites from the original file
    _cards_faces: dict[str, pygame.Surface]  # the scaled cards sprites [cardname: sprite]
    _stacks_locations: dict[str, tuple[int, int, bool]]  # (x, y, V(True)/H)
    _tableau_stacks_cards_quantity: dict[str, int]
    _collision_areas: dict[str, list[tuple[pygame.Rect, str]]]  # {stack: } [(x,y,w,h),  card__str__ )
    _tableau_cards_shift: int  # the shift of the tableau card from the previous card of the same tableau stack
    _is_moving: bool
    
    
    def __init__(self) -> None:
        self._screen_dimensions = (GAME_WIDTH, GAME_HEIGHT)
        self._card_dimensions = (0,0)
        self._cards_faces = {}
        self._stacks_locations = {}
        self._collision_areas = {
            "crapette": [],
            "remainder": [],
            "bin": [],
            "player_tableau0": [],
            "player_tableau1": [],
            "player_tableau2": [],
            "player_tableau3": [],
            "player_foundation0":   [],
            "player_foundation1":   [],
            "player_foundation2":   [],
            "player_foundation3":   [],
            "opponent_tableau1": [],
            "opponent_tableau2": [],
            "opponent_tableau3": [],
            "opponent_tableau0": [],
            "opponent_foundation0":   [],
            "opponent_foundation1":   [],
            "opponent_foundation2":   [],
            "opponent_foundation3":   [],
        }
        self._tableau_stacks_cards_quantity = {
            "player_tableau0": 1,
            "player_tableau1": 1,
            "player_tableau2": 1,
            "player_tableau3": 1,
            "opponent_tableau0": 1,
            "opponent_tableau1": 1,
            "opponent_tableau2": 1,
            "opponent_tableau3": 1,
        }
        self._is_moving = False
     
    @property
    def surface(self) -> pygame.Surface:
        return self._surface
    
    @surface.setter
    def surface(self, surface: pygame.Surface) -> None:
        """returns the game screen that the game is rendered on

        Args:
            surface (pygame.Surface): the game screen window
        """
        self._surface = surface
           
    @property
    def stacks_locations(self) -> dict[str, tuple[int, int, bool]]:
        """The calculated location of the base of the stack on the game screen

        Returns:
            dict[str, tuple[int, int, bool]]: 
                dictionary of:
                    stack name: 
                        top left corner x offset, 
                        top left corner y offset, 
                        Vertical layout of the stack (True) or Horizontal layout    
        """
        return self._stacks_locations
    
    @stacks_locations.setter
    def stacks_locations(self, stacks_locations: dict[str, tuple[int, int, bool]]) -> None:
        """Sets the stacks locations calculated for the current screen

        Args:
            stacks_locations (dict[str, tuple[int, int, bool]]): 
                dictionary of:
                    stack name: 
                        top left corner x offset, 
                        top left corner y offset, 
                        Vertical layout of the stack (True) or Horizontal layout  
        """
        self._stacks_locations = stacks_locations
        self._calculate_collision_areas()
        
    def _calculate_collision_areas(self) -> None:
        """Calculate the collision areas for the stacks
        This is calculated from 
            the stacks location,
            the card dimensions and
            the card shift from the previous card (for the tableau), if needed
        """
        self._collision_areas = {
            "player_crapette": [],
            "player_remainder": [],
            "player_bin": [],
            "player_tableau0": [],
            "player_tableau1": [],
            "player_tableau2": [],
            "player_tableau3": [],
            "player_foundation0":   [],
            "player_foundation1":   [],
            "player_foundation2":   [],
            "player_foundation3":   [],
            "opponent_crapette": [],
            "opponent_remainder": [],
            "opponent_bin": [],
            "opponent_tableau0": [],
            "opponent_tableau1": [],
            "opponent_tableau2": [],
            "opponent_tableau3": [],
            "opponent_foundation0":   [],
            "opponent_foundation1":   [],
            "opponent_foundation2":   [],
            "opponent_foundation3":   [],
        }

        # Calculate the collision areas for the stacks
        for stack in self._stacks_locations:
            col_area = pygame.Rect(
                    self._stacks_locations[stack][0], #  x
                    self._stacks_locations[stack][1], #  y
                    self.card_width,   #  w
                    self.card_height    #  h
                    )
            
            # crapette, remainder, bin and fondation can only be hit in one place
            if stack[:-1] != "player_tableau" or stack[:-1] != "opponent_tableau":
                self._collision_areas[stack].append((col_area, ""))
            
            # tableau cards shift so multiple cards can be picked, so there are multiple 
            # collision areas are needed depending on which card we pick
            else:
                self._collision_areas[stack] =[]
                tableau_card_quantity: int = self._tableau_stacks_cards_quantity[stack]
                # If there are several cards on the tableau, the cards above the base as shiftted, 
                # right for player, left for opponent
                # only the top card will be fully colliding, 
                for card_num in range(tableau_card_quantity):
                    if stack[:-1] == "player_tableau":
                        col_area.x += self._tableau_cards_shift
                    else:
                        col_area.x -= self._tableau_cards_shift
                    
                    # the cards below the top card can only be hit over the shift area
                    if card_num  < tableau_card_quantity:
                        col_area.w = self._tableau_cards_shift
                        
                    # in addition, the opponent tableau shifts to the right,
                    # so the collision happens on the right side of the card
                    if stack[:-1] == "opponent_tableau":
                        col_area.x += self.card_width - self.tableau_cards_shift
                            
                    self._collision_areas[stack].append((col_area, ""))
                      
    @property
    def collision_areas(self) -> dict[str, list[tuple[pygame.Rect, str]]]:
        """returns the collision areas
        Its value is recalculated before it is returned

        Returns:
            dict[str, list[tuple[pygame.Rect, str]]]: 
            dictionary of:
                    stack name:
                        pygame Rect (x, y, w, h) of the collision area
                        card name (str) of the card that is in the collision area
        """
        self._calculate_collision_areas()
        return self._collision_areas
    
        
    # def modify_collision_area_card(self, stack_name: str, new_rect: pygame.Rect, card_name: str) -> None:
    #     card_found = False
    #     reversed_stack = self._collision_areas[stack_name].copy()
    #     reversed_stack.reverse()
    #     for (ca_rect, ca_card) in reversed_stack:
    #         if ca_rect == new_rect:
    #             # if the card has not yet been found in this rectanglle
    #             if not card_found:
    #                 card_found  = True
    #                 self._collision_areas[stack_name].remove((ca_rect, ca_card))
    #                 self._collision_areas[stack_name].append((new_rect, card_name))
    #             else:
    #                 self._collision_areas[stack_name].remove((ca_rect, ca_card))
    #                 self._collision_areas[stack_name].append((new_rect, ""))
    
    @property
    def card_width(self) -> int:
        """The width of the card (vertical) proportional to the window size"""
        return self._card_dimensions[0]
    
    @property
    def card_height(self) -> int:
        """The height of the card (horizontal) proportional to the window size"""
        return self._card_dimensions[1]
                    
    def scale_card_dimensions(self) -> None:
        """
        Set the dimensions of the card faces for the game size
        The size will retain the proportion of the original graphic
        
        Args:
            None
        
        Returns:
            Nothing
        """
        h: int = self.screen_height // 7
        w: int = h * CARD_IMG_WIDTH // CARD_IMG_HEIGHT
        
        self._card_dimensions = (w, h)
      
    @property
    def card_dimensions(self) -> tuple[int, int]:
        """Dimensions of the card for the size of the window

        Returns:
            tuple[int, int]: width, height
        """
        if self._card_dimensions == (0, 0):
            self.scale_card_dimensions()
        return self._card_dimensions
    
    @card_dimensions.setter
    def card_dimensions(self, new_dimensions: tuple[int, int]) -> None:
        """Store the recalculated card dimensions for the size of the window

        Args:
            dimensions (tuple[int, int]): 
                calculated (width, height) of the card sprite for the current screen dimension
        """
        self._card_dimensions = new_dimensions
        
    def _calculate_tableau_cards_shift(self) -> None:
        """
        Calculate the shift of the tableau cards from the previous card of the same tableau stack
        """
        self._tableau_cards_shift = self.card_dimensions[0] // 4
        
    @property
    def tableau_cards_shift(self) -> int:
        """The shift of the tableau card from the previous card of the same tableau stack

        Returns:
            int: the shift in pixels
        """
        self._calculate_tableau_cards_shift()
        return self._tableau_cards_shift
    
    @tableau_cards_shift.setter
    def tableau_cards_shift(self, new_shift: int) -> None:
        self._tableau_cards_shift = new_shift
    
    
    
    
    @property
    def screen_dimensions(self) -> tuple[int, int]:
        return self._screen_dimensions
    
    @screen_dimensions.setter
    def screen_dimensions(self, new_dimensions: tuple[int, int]) -> None:
        self._screen_dimensions = new_dimensions
        self.scale_card_dimensions
        
        
    @property
    def screen_width(self) -> int:
        return self._screen_dimensions [0]
    
    @property
    def screen_height(self) -> int:
        return self._screen_dimensions[1]
    
    def on_window_resize(self, new_dimension: tuple[int, int]):
        self._screen_dimensions = new_dimension
        self._card_dimensions = (0,0)
        
    def card_face(self, card_name: str) -> pygame.Surface:
        """Returns the card sprite for the given card name"""
        return self._cards_faces[card_name]
    
    @property
    def cards_faces(self) -> dict[str, pygame.Surface]:
        return self._cards_faces
    
    
    def scale_cards_faces(self) -> None:
        
        scaled_faces: dict[str, pygame.Surface] = {}
        # print(f"{self.card_dimensions=}")
        
        for card_face in self._originally_loaded_cards_faces:
            scaled_faces[card_face] = pygame.transform.smoothscale( \
                                        self._originally_loaded_cards_faces[card_face],
                                        self.card_dimensions)
        
        self._cards_faces = {}
        self._cards_faces = scaled_faces.copy()