from enum import Enum
import os
import pygame

# The enum representing the players
class Players(Enum):
    PLAYER1 = 0
    PLAYER2 = 1
    CARDSTACK = 2 # mostly for debugging purposes for the moment
    ERROR = -1
    
# dimensions of the game window
GAME_WIDTH: int = 1024
GAME_HEIGHT: int = 768

# icon of the game
IMAGES_DIR: str = os.path.dirname(os.path.abspath(__file__)) + "/img/"
CARD_FACES_DIR: str = os.path.join(IMAGES_DIR, "card_faces")
GAME_ICON_FILE: str = os.path.join(IMAGES_DIR, "two_backs_256x256.png")
GAME_ICON: pygame.Surface = pygame.image.load(GAME_ICON_FILE)
# GAME_ICON: pygame.Surface = pygame.image.load("img/two_backs_256x256.png")