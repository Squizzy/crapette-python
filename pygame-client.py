import pygame
import os

# dimensions of the game window
GAME_WIDTH: int = 1024
GAME_HEIGHT: int = 768

# icon of the game
IMAGES_DIR: str = os.path.dirname(os.path.abspath(__file__)) + "/img/"
CARD_FACES_DIR: str = os.path.join(IMAGES_DIR, "card_faces")
GAME_ICON_FILE: str = os.path.join(IMAGES_DIR, "two_backs_256x256.png")
GAME_ICON: pygame.Surface = pygame.image.load(GAME_ICON_FILE)
# GAME_ICON: pygame.Surface = pygame.image.load("img/two_backs_256x256.png")

# Initialising background colours
FELT_GREEN = (0, 96, 0) # felt dark green 
FELT_RED = (96, 0, 0) # felt dark red 
FELT_BLUE = (0, 0, 96) # felt dark blue 
YELLOW = (255, 255, 0) # yellow 

# dimensions of the image files
# objective value based on the graphics files used for th game
# TODO: this is for the png I am currently using -  eventually might be better to scan all files or store the values in a config file?
CARD_IMG_HEIGHT: int = 333
CARD_IMG_WIDTH: int = 234




    
# card_scale_landscape: float = GAME_HEIGHT / 7  # Assuming landscape mode is used - might have to adjust using GAME_WIDTH if portrait mode is used?
# # card_scale_portrait: float = GAME_WIDTH / 7 ## Value not verified or used yet

# # desired dimension of the images on the screen
# card_game_height: int = int(card_scale_landscape)
# card_game_width: int = int(CARD_IMG_WIDTH * card_game_height / CARD_IMG_HEIGHT)


# Stores a copy of the game state from the server
# Updates from the server
class GameState:
    _stacks: dict[str, list[str]]
    _turn_player: int
    
    def __init__(self) -> None:
        self._stacks = {
            "player_crapette":      [],
            "player_remainder":     [],
            "player_bin":           [],
            "player_tableau":       [],
            "player_foundation":    [],
            "opponent_crapette":    [],
            "opponent_remainder":   [],
            "opponent_bin":         [],
            "opponent_tableau":     [],
            "opponent_foundation":  [],
        }
        

class Cards:
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
        # Get the directory of the script
        # card_faces_images_dir = os.path.dirname(os.path.abspath(__file__)) + "/img/card_faces"
        
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
        for card in other_cards_list:
            if card + ".png" not in png_files:
                raise ValueError(f"Card {card} not found in {CARD_FACES_DIR}")
        
        # svg_files = [f for f in os.listdir(card_faces_images_dir) if f.endswith('.svg')]
        # card_name: str
        for card in play_cards_list:
            # card_name = card.split(".")[0]            
            # print(f"Loading card: {card}")
            # if the card file does not correspond to a card that we want, skip it
            # if card_name not in play_cards_list:
            #     print(f"Skipping card: {card_name}")
            #     continue
            
            # Load the card face into the card_faces dictionary
            try: 
                # card_faces[card[0] + card[1]] = pygame.image.load(card_faces_images_dir + "/" + card)
                cards_faces[card] = pygame.image.load(os.path.join(CARD_FACES_DIR, f"{card}.svg"))
            # except FileNotFoundError:
            #     raise ValueError(f"Card {card} not found in {CARD_FACES_DIR}")
            except pygame.error as e:
                raise ValueError(f"Card {card} not loaded: {e}")

        # add back_blue, back_red, empty_card
        for card in other_cards_list:
            try:
                # for card in other_cards_list:
                cards_faces[card] = pygame.image.load(os.path.join(CARD_FACES_DIR, f"{card}.png"))
                # self._cards_faces["BB"] = pygame.image.load(os.path.join(CARD_FACES_DIR, "BB.png"))
                # self._cards_faces["BR"] = pygame.image.load(os.path.join(CARD_FACES_DIR, "BR.png"))
                # self._cards_faces["EC"] = pygame.image.load(os.path.join(CARD_FACES_DIR,  "EC.png"))
                # except FileNotFoundError:
                #     raise ValueError(f"Card BB, BR  or EC not found in {CARD_FACES_DIR}")
            except pygame.error as e:
                raise ValueError(f"Card BB, BR or EC not loaded: {e}")
        
        # card_faces["BB"] = pygame.image.load(card_faces_images_dir + "/BB.png")
        # card_faces["BR"] = pygame.image.load(card_faces_images_dir + "/BR.png")
        # card_faces["EC"] = pygame.image.load(card_faces_images_dir + "/EC.png")
            
        if len(cards_faces) != len(play_cards_list) + len(other_cards_list):
            raise ValueError(f"card images problem: only {len(cards_faces)} cards loaded, expected {len(play_cards_list) + len(other_cards_list)}")

        # Convert each card faces to a surface
        for card in cards_faces:
            cards_faces[card].convert()

        self._originally_loaded_cards_faces = cards_faces.copy()
    
    def _scale_cards_dimensions(self, screen_height: int) -> None:
        """
        Calculate the scaled dimensions of the cards
        
        Returns:
            Nothing
        """
        self._height = screen_height // 7
        self._width = self._height * CARD_IMG_WIDTH // CARD_IMG_HEIGHT

    def scale_cards_faces(self, screen_height: int) -> None:
        """
        Scale the card faces to the game size
        
        Returns:
            Nothing
        """
        self._scale_cards_dimensions(screen_height)
        
        self._cards_faces = {}
        for card in self._originally_loaded_cards_faces:
            # Convert the card faces to a surface
            # self._cards_faces[card].convert()
            
            # Scale the card faces to the game size
            self._cards_faces[card] = pygame.transform.smoothscale( \
                                        # self._cards_faces[card], 
                                        self._originally_loaded_cards_faces[card], 
                                        (self.width, self.height))

        # Make the EC card transparent
        self._cards_faces["EC"].set_colorkey(self._originally_loaded_cards_faces["EC"].get_at((50,50)))
    
class StacksLayout:
    _screen_width: int
    _screen_height: int
    _center_x: int
    _center_y: int
    _margin_x: int
    _margin_y: int
    _cards:  Cards
    
    def __init__(self, cards: Cards) -> None:
        """
        Initialise the stacks layout
        Calculate the positions of the stacks
        Store the positions in the _positions attribute
        """
        self._screen_width = GAME_WIDTH
        self._screen_height = GAME_HEIGHT
        
        self._cards = cards
        # self._card_width = cards.card_width
        # self._card_height = cards.card_height
        # , self._card_height = scaled_cards_dimensions(GAME_HEIGHT)
        
        # self._margin_x = self._card_width // 7
        # self._margin_y = self._card_height // 7
        # self._center_x = self._screen_width // 2
        # self._center_y = self._screen_height // 2
        self._margin_x = self._cards.width // 7
        self._margin_y = self._cards.height // 7
        self._center_x = self._screen_width // 2
        self._center_y = self._screen_height // 2
                
        self._positions = self._calculate_positions()
        
    @property
    def stacks_positions(self) -> dict[str, tuple[int, int, bool]]:
        """ 
        Get the positions of the stacks
        
        Returns:
            dict[str, tuple[int, int, bool]]: a dictionary containing:
                - key: the name of the stack
                - values:
                    - the top left corner coordinate of the bottom of the stack x, y
                    - a boolean indicating if the card is placed vertically or horizontally
        """
        return self._positions
    
    def set_screen_dimensions(self, screen_width: int, screen_height: int) -> None:
        self._screen_width = screen_width
        self._screen_height = screen_height
        
    def _calculate_positions(self) -> dict[str, tuple[int, int, bool]]:
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
        # x positions (top left corner)
        player_center_x = self._center_x - self._cards.width // 2
        player_left_x = player_center_x - self._cards.width - self._margin_x
        player_right_x = player_center_x + self._cards.width + self._margin_x
        player_foundation_x = self._center_x + self._margin_x
        player_tableau_x = player_foundation_x + self._margin_x + self._cards.height
        
        opponent_center_x = self._center_x - self._cards.width // 2
        opponent_left_x = opponent_center_x - self._cards.width - self._margin_x
        opponent_right_x = opponent_center_x + self._cards.width + self._margin_x
        opponent_foundation_x = self._center_x - self._margin_x - self._cards.height
        opponent_tableau_x = opponent_foundation_x - self._margin_x - self._cards.width
        
        # y positions (top left corner)
        opponent_y = self._center_y - self._cards.height * 3 - int(self._margin_y * 2.5)
        player_y = self._center_y + self._cards.height * 2 + int(self._margin_y * 2.5)
        tableau_top_y = self._center_y - self._cards.height * 2 - int(self._margin_y * 1.5)
        foundation_top_y = tableau_top_y + (self._cards.height - self._cards.width) //2
        tableau_spacing_y = self._cards.height + self._margin_y
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
            center_stacks_positions[f"opponent_tableau_{o}"] = (opponent_tableau_x, tableau_top_y + tableau_spacing_y * o, True)
            center_stacks_positions[f"opponent_foundation_{o}"] = (opponent_foundation_x, foundation_top_y + tableau_spacing_y * o, False)
            center_stacks_positions[f"player_tableau_{p}"] = (player_tableau_x, tableau_top_y + tableau_spacing_y * p, True)
            center_stacks_positions[f"player_foundation_{p}"] = (player_foundation_x, foundation_top_y + tableau_spacing_y * p, False)

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
        stacks_positions = opponent_base_stacks_positions |center_stacks_positions | player_base_stacks_positions    
        return stacks_positions
    
    
    def stacks_reposition_and_resize(self, width: int, height: int, cards: Cards) -> None:
        """
        Resize the screen
        Recalculate the positions of the stacks
        """
        print(f"Screen Resize: {width=}, {height=}")
        # update the screen dimensions
        self._screen_width = width
        self._screen_height = height
        self._center_x = self._screen_width // 2
        self._center_y = self._screen_height // 2
        
        # update the card dimensions
        self._cards = cards
        self._cards.scale_cards_faces(height)
        # self._card_width = cards.card_width
        # self._card_height = cards.card_height
        # self._margin_x = self._card_width // 7
        # self._margin_y = self._card_height // 7
        # self._cards.width = cards.width
        # self._card_height = cards.card_height
        self._margin_x = self._cards.width // 7
        self._margin_y = self._cards.height // 7
        self._positions = self._calculate_positions()


card_faces: dict[str, pygame.Surface] = {}
clock: pygame.time.Clock = pygame.time.Clock()

def pygame_init():
    # Initialise pygame
    pygame.init()
    # (numpass, numfail) = pygame.init()
    # print(f"{numpass=}, {numfail=}")

def window_init() -> pygame.Surface:
    # Set up the game window
    surface: pygame.Surface = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), pygame.RESIZABLE)

    # Set title of window
    pygame.display.set_caption("pygame title")

    # Set icon if window
    pygame.display.set_icon(GAME_ICON)

    # Changing the surface colour
    surface.fill(FELT_GREEN)
    return surface

def server_get_stacks_cards():
    #TODO: Implement the server_get_stacks_cards function - use get_stacks_cards_from_server() instead?
    ...
    
def player_stacks_init(player: int):

    # create the stacks dictionary
    stacks_cards: dict[str, list[str]] = {
        "player_crapette":      [],
        "player_remainder":     [],
        "player_bin":           [],
        "player_tableau":       [],
        "player_foundation":    [],
        "opponent_crapette":    [],
        "opponent_remainder":   [],
        "opponent_bin":         [],
        "opponent_tableau":     [],
        "opponent_foundation":  [],
    }
    
    server_stacks_cards = server_get_stacks_cards()
    # TODO: convert the server_stacks_cards to the stacks_cards dictionary
    return stacks_cards





def place_stacks(surface: pygame.Surface, stacks_layout: StacksLayout, cards: Cards):
    stacks_positions = stacks_layout.stacks_positions
    # stacks_positions = StacksLayout().stacks_positions
    
    # for stack in stacks_positions:
    #     blit_blank = cards.card_faces["EC"] if stacks_positions[stack][2] \
    #         else pygame.transform.rotate(cards.card_faces["EC"].copy(), 90)

    #     surface.blit(blit_blank, (stacks_positions[stack][0], stacks_positions[stack][1]) )
    
    # stacks_positions = StacksLayout().stacks_positions
    
    for stack in stacks_positions:
        blit_blank = cards.faces["EC"] if stacks_positions[stack][2] \
            else pygame.transform.rotate(cards.faces["EC"].copy(), 90)

        surface.blit(blit_blank, (stacks_positions[stack][0], stacks_positions[stack][1]) )

def update_stacks(surface: pygame.Surface):
    #TODO: Implement the update_stacks function
    ...

def game_loop(surface: pygame.Surface, stacks_layout: StacksLayout, cards: Cards):
    
    # clock = pygame.time.Clock()

    blit_card = cards.faces["HQ"]
    # blit_card_width = card_faces["HQ"].get_width()
    # blit_card_height = card_faces["HQ"].get_height()
    # blit_card_angle = 0

    rect: pygame.Rect = blit_card.get_rect()
    # rect: pygame.Rect = card_faces["HQ"].get_rect()
    # surface.blit(blit_card, (100, 100))

    color = FELT_GREEN
    # Game loop 
    running = True
    moving = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # print("Button Down")
                # rect = blit_card.get_rect()
                if rect.collidepoint(event.pos):
                    # print("Collision detected")
                    moving = True
            elif event.type == pygame.MOUSEBUTTONUP:
                # print("Button Up")
                moving = False
            elif event.type == pygame.MOUSEMOTION and moving:
                # print(f"Mouse Move: {rect.x=}, {rect.y=}")
                rect.move_ip(event.rel)
            elif event.type == pygame.K_ESCAPE:
                print("Key q detected")
                running = False
                
            elif  event.type == pygame.VIDEORESIZE:
                # print(f"Video Resize: {event.size=}")
                print("redimensioning")
                surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                # stacks_layout.set_screen_dimensions(int(event.w), int(event.h))
                stacks_layout.stacks_reposition_and_resize(event.w, event.h, cards)
            else:
                pass
        
        # set background colour
        # color = FELT_RED if color == FELT_GREEN else FELT_GREEN
        surface.fill(color)
        
        # place empty cards in the stacks positions
        place_stacks(surface, stacks_layout, cards)
        
        # Make a circle
        # pygame.draw.circle(surface, (FELT_BLUE), (GAME_WIDTH/2, GAME_HEIGHT/2), 75)

        # Make a rectangle
        # this_rect = pygame.draw.rect(surface, color=YELLOW, rect=pygame.Rect(30, 30, 60, 60))

        # print("blitting")
        # surface.blit(blit_card, rect)

        # scaling
        # blit_card_width = int(blit_card_width * 0.99)
        # blit_card_height = int(blit_card_height * 0.99)
        # blit_card = pygame.transform.smoothscale(card_faces["HQ"], (blit_card_width, blit_card_height))

        # rotating
        # blit_card_angle = blit_card_angle + 3
        # blit_card = pygame.transform.rotate(blit_card, blit_card_angle)
        # card_faces["HQ"] = pygame.transform.scale(card_faces["HQ"], (int(card_faces["HQ"].get_size()[0]*0.99), int(card_faces["HQ"].get_size()[1]*0.99)))

        # surface.blit(card_faces["EC"], (120, 120))

        # update the window
        # pygame.display.update()
        pygame.display.flip()
        pygame.time.delay(100)

        # clock.tick(3000)


    pygame.quit()


if __name__ == "__main__":
    pygame_init()
    surface: pygame.Surface = window_init()
    cards: Cards = Cards(GAME_HEIGHT)
    stacks_layout: StacksLayout = StacksLayout(cards)
    # stacks_cards: dict[str, list[str]] = player_stacks_init(1)
    # load_card_faces()
    game_loop(surface, stacks_layout, cards)
