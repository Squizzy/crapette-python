import pygame
import os

from constants import GAME_HEIGHT, CARD_FACES_DIR, Players
from client_game_state import GameState
from client_ui_game_state import UIGameState
from game_logger import GameLogger

client_logger: GameLogger


# dimensions of the image files
# objective value based on the graphics files used for th game
# TODO: this is for the png I am currently using
# -  eventually might be better to scan all files or store the values in a config file?
CARD_IMG_HEIGHT: int = 333
CARD_IMG_WIDTH: int = 234

class CardsUI:
    _game_state: GameState
    _ui_game_state: UIGameState
    
    # _cards_faces: dict[str, pygame.Surface]
    _originally_loaded_cards_faces: dict[str, pygame.Surface]
    _width: int
    _height: int
    
    def __init__(self, logger: GameLogger, client_game_state: GameState, client_game_ui_state: UIGameState, screen_height: int = GAME_HEIGHT) -> None:
        global client_logger
        client_logger = logger
        
        self._game_state = client_game_state
        self._ui_game_state = client_game_ui_state
        
        self._ui_game_state._cards_faces = {}
        self._load_cards_faces()
        client_logger.info("card faces loaded")
        
        self._cards_faces = self._originally_loaded_cards_faces.copy()
        self.scale_cards_faces(screen_height)
        client_logger.info("initial cards scaling done")
        
    @property
    def faces(self) -> dict[str, pygame.Surface]:
        return self._cards_faces
    
    @property
    def width(self) -> int:
        return self._width
    
    @property
    def height(self) -> int:
        return self._height
    
    def _load_cards_faces(self) -> None:
        """
        Load the card faces into the cards_faces dictionary
        The cards_faces dictionary is used to store the card faces as self._originally_loaded_cards_faces
        The rescaling will always come from this dictionary to ensure consistent quality

        Raises:
            ValueError: If a svg file (card face) is missing
            ValueError: If a png file (card back or blank) is missing
            ValueError: If a svg file was not loaded correctly
            ValueError: If a png file was not loaded correctlty
            ValueError: If the dictonary ends up with the incorrect number of card faces
        """
        
        # dictionary to store the card faces
        cards_faces: dict[str, pygame.Surface] = {}
        
        # list of the card faces to load
        play_cards_list: list[str] = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "CJ", "CQ", "CK",
                                      "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "DJ", "DQ", "DK",
                                      "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "HJ", "HQ", "HK",
                                      "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "SJ", "SQ", "SK"]
        other_cards_list: list[str] = ["BB", "BR", "EC"]
        
        # Get the list of all SVG files in the directory
        # Currently the card faces only are in SVG format
        svg_files: list[str] = [f for f in os.listdir(CARD_FACES_DIR) if f.endswith('.svg')]
        
        # check that all the card faces files can be found.  (at least as filenames)
        for card in play_cards_list:
            if card + ".svg" not in svg_files:
                raise ValueError(f"Card {card} not found in {CARD_FACES_DIR}")
        
        # Get the list of all PNG files in the directory
        # Currently the card backs and empty card only are in PNG format
        png_files: list[str] = [f for f in os.listdir(CARD_FACES_DIR) if f.endswith('.png')]
        
        # check that all the card faces files can be found.  (at least as filenames)
        for card in other_cards_list:
            if card + ".png" not in png_files:
                raise ValueError(f"Card {card} not found in {CARD_FACES_DIR}")
        
        # For each card in the play_cards_list...
        for card in play_cards_list:
            
            # Load the card graphics into the card_faces dictionary
            try: 
                cards_faces[card] = pygame.image.load(os.path.join(CARD_FACES_DIR, f"{card}.svg"))
            except pygame.error as e:
                raise ValueError(f"Card {card} not loaded: {e}")

        # for the cards in the other_cards_list
        for card in other_cards_list:
            
            # Load the card graphics into the card_faces dictionary
            try:
                cards_faces[card] = pygame.image.load(os.path.join(CARD_FACES_DIR, f"{card}.png"))
            except pygame.error as e:
                raise ValueError(f"Card BB, BR or EC not loaded: {e}")
            
        # Double check that all cards have a graphics associated
        if len(cards_faces) != len(play_cards_list) + len(other_cards_list):
            raise ValueError(f"card images problem: only {len(cards_faces)} cards loaded, expected {len(play_cards_list) + len(other_cards_list)}")

        # Convert each card face to a pygame surface
        for card in cards_faces:
            cards_faces[card] = cards_faces[card].convert()

        # Store this as the original dictionary to ensure consistent quality
        self._originally_loaded_cards_faces = cards_faces.copy()
    
    def _scale_cards_dimensions(self, screen_height: int) -> None:
        """
        Set the dimensions of the card faces for the game size
        The size will retain the proportion of the original graphic
        
        Args:
            screen_height (int): the height of the game window
        
        Returns:
            Nothing
        """
        self._height = screen_height // 7
        self._width = self._height * CARD_IMG_WIDTH // CARD_IMG_HEIGHT

    def scale_cards_faces(self, screen_height: int) -> None:
        """
        Scale the card faces to the game size
        Method is called by other objects when resizing the game window
        
        Returns:
            Nothing
        """
        self._scale_cards_dimensions(screen_height)
        
        # Clear the cards faces graphics for the active game
        self._ui_game_state._cards_faces = {}
        
        # For each card graphic as it was originally loaded from the images...
        for card in self._originally_loaded_cards_faces:
            
            # Scale the card faces to the game size
            self._ui_game_state._cards_faces[card] = pygame.transform.smoothscale( \
                                        self._originally_loaded_cards_faces[card], 
                                        (self.width, self.height))

        # Make the EC card transparent
        self._cards_faces["EC"].set_colorkey(self._ui_game_state._cards_faces["EC"].get_at((3,3)))
        
        # self._ui_game_state._cards_faces = self._cards_faces.copy()
    
    def place_card(self, this_player: int, stack: str, card: str) -> None:
        """
        Place a card on the screen

        Args:
            screen (pygame.surface): the main display area for the game
            player (int): the player whose turn it is
            stack (str): the stack where the card is located
            card (str): the card to be placed
        """

        # cards contains Suit [1 char] Rank [1 or 2 char] face_up [1 char] 
        card_face: str = card[:-1]
        # client_logger.debug(f"{card=} -> {card_face=}")
        
        # Calculate the position of the card on the screen
        player: int = self._game_state.player_id.value        
        stack_prefix = "player_" if this_player == player else "opponent_"

        # client_logger.debug(f"{stack_prefix=} {stack=}")
        (x, y, vertical) = self._ui_game_state.stacks_locations[stack_prefix + stack]
        # client_logger.debug(f"({x}, {y}, {vertical})")
        

        if card[:1]:  # face up
            card_graphic = self._ui_game_state._cards_faces[card_face]
        else:
            card_graphic = self._ui_game_state._cards_faces["BB" if player ==  0 else "BR"] # if player == 0 else self._ui_game_state._cards_faces["BR"] 
    
        # blit_card = self._ui_game_state._cards_faces[card_face] if vertical \
        #             else pygame.transform.rotate(self._ui_game_state._cards_faces[card_face].copy(), 90)
            
        blit_card = card_graphic if vertical else pygame.transform.rotate(card_graphic.copy(), 90)
        
        self._ui_game_state._surface.blit(blit_card, (x, y) )

    def place_stack(self,   this_player: int, stack_name: str,  cards_list: list[str]) -> None:
        
        
        # Calculate the position of the card on the screen
        player: int = self._game_state.player_id.value   
             
        stack_prefix = "player_" if this_player == player else "opponent_"
        (x, y, vertical) = self._ui_game_state.stacks_locations[stack_prefix + stack_name]
        
        shift: int = self.width // 4
        
        cards_blits = []
        
        for card in cards_list:    
            # cards contains Suit [1 char] Rank [1 or 2 char] face_up [1 char] 
            card_face: str = card[:-1]

            # client_logger.debug(f"{player=} {this_player=}")
            
            if card[-1] == 'u':  # face up
                card_graphic = self._ui_game_state._cards_faces[card_face]
            else:
                card_graphic = self._ui_game_state._cards_faces["BB" if this_player == player else "BR"] # self._ui_game_state._cards_faces["BR"] 
        # if this_player == 1 else "BR"]
            # blit_card = self._ui_game_state._cards_faces[card_face] if vertical \
            #             else pygame.transform.rotate(self._ui_game_state._cards_faces[card_face].copy(), 90)
                
            cards_blits.append(card_graphic if vertical else pygame.transform.rotate(card_graphic.copy(), 90))
        
        for card_blit in cards_blits:
            self._ui_game_state._surface.blit(card_blit, (x, y) )
            
            if stack_name[:-1] == "tableau" and this_player == player:
                x += shift
                
            if stack_name[:-1] == "tableau" and this_player != player:
                x -= shift
                
            if stack_name == "crapette" and this_player == player:
                x -= shift
                
            if stack_name == "crapette" and this_player != player:
                x += shift
                
                

    # def place_stacks_cards(self, stacks: dict[int, dict[str, list[str]]]) -> None:
    def place_stacks_cards(self) -> None:
        stacks: dict[str, dict[str, list[str]]] = self._game_state.stacks_cards
        player = self._game_state.player_id.value
        opponent = 1 - player
        
        # client_logger.debug(f"HERE: {player=}: {Players(player).name}")
        # client_logger.debug(f"{stacks}")
        
        # our cards
        for stack_name, card_stack in stacks[Players(player).name].items():
            # client_logger.debug(f"stack: {stack} : {stacks[Players(player).name][stack]}")
            # for stack_name, card_stack in stacks[Players(player).name][stack].items():
                self.place_stack(player, stack_name, card_stack)
                # client_logger.debug(f"{card}")
                # self.place_card(player, stack, card)
                
        # #opponent cards
        for stack_name, card_stack in stacks[Players(opponent).name].items():
            self.place_stack(opponent, stack_name, card_stack)

        # for stack in stacks[Players(opponent).name]:
        #     for card in stacks[Players(opponent).name][stack]:
        #         self.place_card(opponent, stack, card)
        