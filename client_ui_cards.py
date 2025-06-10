import pygame
import os

from constants import GAME_HEIGHT, CARD_FACES_DIR


# dimensions of the image files
# objective value based on the graphics files used for th game
# TODO: this is for the png I am currently using
# -  eventually might be better to scan all files or store the values in a config file?
CARD_IMG_HEIGHT: int = 333
CARD_IMG_WIDTH: int = 234

class CardsUI:
    _cards_faces: dict[str, pygame.Surface]
    _originally_loaded_cards_faces: dict[str, pygame.Surface]
    _width: int
    _height: int
    
    def __init__(self, screen_height: int = GAME_HEIGHT) -> None:
        self._cards_faces = {}
        self._load_cards_faces()
        self._cards_faces = self._originally_loaded_cards_faces.copy()
        self.scale_cards_faces(screen_height)
        
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
        self._cards_faces = {}
        
        # For each card graphic as it was originally loaded from the images...
        for card in self._originally_loaded_cards_faces:
            
            # Scale the card faces to the game size
            self._cards_faces[card] = pygame.transform.smoothscale( \
                                        self._originally_loaded_cards_faces[card], 
                                        (self.width, self.height))

        # Make the EC card transparent
        self._cards_faces["EC"].set_colorkey(self._cards_faces["EC"].get_at((3,3)))
    
    