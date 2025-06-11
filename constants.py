from enum import Enum
import os
import pygame

# The enum representing the players
class Players(Enum):
    PLAYER0 = 0
    PLAYER1 = 1
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

class TableColours:
    # Initialising background colours
    FELT_GREEN = (0, 96, 0) # felt dark green 
    FELT_RED = (96, 0, 0) # felt dark red 
    FELT_BLUE = (0, 0, 96) # felt dark blue 
    YELLOW = (255, 255, 0) # yellow 

class TextColours:
    
    # FOREGROUND
    # Basic colors
    BLACK = "\x1b[30m"
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    BLUE = "\x1b[34m"
    MAGENTA = "\x1b[35m"
    CYAN = "\x1b[36m"
    DARK_WHITE = "\x1b[37m"
    
    # # Bold Basic colours
    # GREY = "\x1b[30;1m"
    # BOLD_RED = "\x1b[31;1m"
    # BOLD_GREEN = "\x1b[32;1m"
    # BOLD_YELLOW = "\x1b[33;1m"
    # BOLD_BLUE = "\x1b[34;1m"
    # BOLD_MAGENTA = "\x1b[35;1m"
    # BOLD_CYAN = "\x1b[36;1m"
    # BOLD_WHITE = "\x1b[37;1m"
    
    # Bright Basic Colours
    GREY = "\x1b[90m"
    ORANGE = "\x1b[91m"
    BRIGHT_GREEN = "\x1b[92m"
    BRIGHT_YELLOW = "\x1b[93m"
    PURPLE = "\x1b[94m"
    BRIGHT_MAGENTA = "\x1b[95m"
    BRIGHT_CYAN = "\x1b[96m"
    WHITE = "\x1b[97m"
    
    # Background colors
    BG_BLACK = "\x1b[40;20m"
    BG_RED = "\x1b[41;20m"
    BG_GREEN = "\x1b[42;20m"
    BG_YELLOW = "\x1b[43;20m"
    BG_BLUE = "\x1b[44;20m"
    BG_MAGENTA = "\x1b[45;20m"
    BG_CYAN = "\x1b[46;20m"
    BG_WHITE = "\x1b[47;20m"
    
    RESET = "\x1b[0m"
    
    
# class colors:


# '''Colors class:reset all colors with colors.reset; two
# sub classes fg for foreground
# and bg for background; use as colors.subclass.colorname.
# i.e. colors.fg.red or colors.bg.greenalso, the generic bold, disable,
# underline, reverse, strike through,
# and invisible work with the main class i.e. colors.bold'''
# reset = '\033[0m'
# bold = '\033[01m'
# disable = '\033[02m'
# underline = '\033[04m'
# reverse = '\033[07m'
#  strikethrough = '\033[09m'
#   invisible = '\033[08m'

#    class fg:
#         black = '\033[30m'
#         red = '\033[31m'
#         green = '\033[32m'
#         orange = '\033[33m'
#         blue = '\033[34m'
#         purple = '\033[35m'
#         cyan = '\033[36m'
#         lightgrey = '\033[37m'
#         darkgrey = '\033[90m'
#         lightred = '\033[91m'
#         lightgreen = '\033[92m'
#         yellow = '\033[93m'
#         lightblue = '\033[94m'
#         pink = '\033[95m'
#         lightcyan = '\033[96m'

#     class bg:
#         black = '\033[40m'
#         red = '\033[41m'
#         green = '\033[42m'
#         orange = '\033[43m'
#         blue = '\033[44m'
#         purple = '\033[45m'
#         cyan = '\033[46m'
#         lightgrey = '\033[47m'