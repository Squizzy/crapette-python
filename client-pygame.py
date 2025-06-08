import pygame
import os
from client_network import ClientConnection
from constants import Players

from icecream import ic
ic.configureOutput(prefix='pygame_client: ')
def log_message(msg:str) -> None:
    DEBUG = True
    if DEBUG:
        ic(msg)

# dimensions of the game window
GAME_WIDTH: int = 1024
GAME_HEIGHT: int = 768

# Initialising background colours
FELT_GREEN = (0, 96, 0) # felt dark green 
FELT_RED = (96, 0, 0) # felt dark red 
FELT_BLUE = (0, 0, 96) # felt dark blue 
YELLOW = (255, 255, 0) # yellow 

# icon of the game
IMAGES_DIR: str = os.path.dirname(os.path.abspath(__file__)) + "/img/"
CARD_FACES_DIR: str = os.path.join(IMAGES_DIR, "card_faces")
GAME_ICON_FILE: str = os.path.join(IMAGES_DIR, "two_backs_256x256.png")
GAME_ICON: pygame.Surface = pygame.image.load(GAME_ICON_FILE)
# GAME_ICON: pygame.Surface = pygame.image.load("img/two_backs_256x256.png")

# dimensions of the image files
# objective value based on the graphics files used for th game
# TODO: this is for the png I am currently using
# -  eventually might be better to scan all files or store the values in a config file?
CARD_IMG_HEIGHT: int = 333
CARD_IMG_WIDTH: int = 234


# Stores a copy of the game state from the server
# Updates from the server
class GameState:
    _player_id: Players
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
        
    @property
    def player_id(self) -> Players:
        return self._player_id
    
    @player_id.setter
    def player_id(self, player: Players) -> None:
        self._player_id = player
        

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
        # Initiate the screen dimensions
        self._screen_width = GAME_WIDTH
        self._screen_height = GAME_HEIGHT
        self._center_x = self._screen_width // 2
        self._center_y = self._screen_height // 2
        
        # Get the cards graphics
        self._cards = cards
        # Initiate the margin between the stacks
        self._margin_x = self._cards.width // 7
        self._margin_y = self._cards.height // 7
        
        # Calculate the positions of the stacks for the screen dimensions
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
    
    # def set_screen_dimensions(self, screen_width: int, screen_height: int) -> None:
    #     self._screen_width = screen_width
    #     self._screen_height = screen_height
        
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
    
    def update_stacks_positions_and_sizes(self, width: int, height: int, cards: Cards) -> None:
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
        self._cards.scale_cards_faces(height)

        # update the margin between the stacks
        self._margin_x = self._cards.width // 7
        self._margin_y = self._cards.height // 7
        
        # calculate the positions of the stacks
        self._positions = self._calculate_positions()

    def render_empty_stacks(self, surface: pygame.Surface, cards: Cards):
        """
        Display the stacks positions using an empty card. 

        Args:
            surface (pygame.Surface): The surface to display on
            cards (Cards): the set of card graphics to use
        """
        stacks_positions = self.stacks_positions
        
        card_face: str = "EC"
        # card_face = "HQ"
        
        for stack in stacks_positions:
            blit_blank = self._cards.faces[card_face] if stacks_positions[stack][2] \
                                        else pygame.transform.rotate(self._cards.faces[card_face].copy(), 90)
            
            surface.blit(blit_blank, (stacks_positions[stack][0], stacks_positions[stack][1]) )


# class Communication:
#     _conn: ClientConnection
#     def __init__(self):
#         self._cc= ClientConnection()
#         self._cc.connect()
        


class Game:
    _surface: pygame.Surface
    _table_colour: tuple[int, int, int]
    _cards: Cards
    _stacks_layout: StacksLayout
    _comm: ClientConnection
    _game_state: GameState
    
    def __init__(self) -> None:
        self._table_colour = FELT_GREEN
        self._pygame_init()
        self._surface = self._window_init()
        self._cards = Cards(GAME_HEIGHT)
        self._stacks_layout = StacksLayout(self._cards)
        self._game_state = GameState()
        
        # connect to the server
        self._comm = ClientConnection()
        self._comm.connect()
        
        # initialise the player id for this client
        self._game_state.player_id = self._comm.request_player_id_from_server()
        log_message(self._game_state.player_id)    
        
        # get the cards from the server and assign them to the game state
        stacks_cards_from_server = self._comm.server_get_stacks_cards()
        
            
        # stacks_cards =  self._comm.server_get_stacks_cards()
        # # self._message_decoder = client_message_decoder()
        # crapette_stack = client_message_decoder.crapette_stack(message=stacks_cards)
        # # crapette_stack = self._message_decoder(stacks_cards)
        # print(crapette_stack)
        

    @property
    def surface(self) -> pygame.Surface:
        return self._surface
    
    @surface.setter
    def surface(self, surface: pygame.Surface) -> None:
        self._surface = surface
    
    @property 
    def cards(self) -> Cards:
        return self._cards
    
    @property 
    def stacks_layout(self) -> StacksLayout:
        return self._stacks_layout

    @property
    def table_colour(self) -> tuple[int, int, int]:
        return self._table_colour

    def _pygame_init(self) -> None:
        """
        Initialize pygame
        """
        pygame.init()

    def _window_init(self) -> pygame.Surface:
        """
        Iniitialiise the game window surface

        Returns:
            pygame.Surface: the main display area for the game
        """
        # Set up the game window
        surface: pygame.Surface = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), pygame.RESIZABLE)

        # Set title of window
        pygame.display.set_caption("pygame title")

        # Set icon if window
        pygame.display.set_icon(GAME_ICON)

        # Change the background
        surface.fill(self.table_colour)
        
        return surface
    
    def _window_resize(self, width: int, height: int, other: int | None) -> None:   
        """
        Resize the game surface and reset its background colour
        Done here so that any game table element can be reset immediately.
        Makes it cleaner for the game loop

        Args:
            width (int): new width of the game window
            height (int): new height of the game window
            other (int | None): another parameter for the resize method
        """
        self._surface = pygame.display.set_mode((width, height), other)
        self._surface.fill(self.table_colour)
        self.stacks_layout.update_stacks_positions_and_sizes(width, height, self.cards)

    def _window_redraw(self):
        """
        Redraw the game screen
        """
        
        # place empty cards in the stacks positions
        self.stacks_layout.render_empty_stacks(self.surface, self.cards)
        
        # update the window
        pygame.display.flip()

    def game_loop(self) -> None:
        """
        The main game loop

        """
        # def game_loop(surface: pygame.Surface, stacks_layout: StacksLayout, cards: Cards):
        # clock: pygame.time.Clock = pygame.time.Clock()

        blit_card = self.cards.faces["HQ"]
        # blit_card_width = card_faces["HQ"].get_width()
        # blit_card_height = card_faces["HQ"].get_height()
        # blit_card_angle = 0

        rect: pygame.Rect = blit_card.get_rect()
        # rect: pygame.Rect = card_faces["HQ"].get_rect()
        # surface.blit(blit_card, (100, 100))

        # color = FELT_GREEN
        
        
        # A card or stack is being displaced
        moving = False

        # Set the game running state
        running = True
        
        # Game loop 
        while running:
            
            # Handle events
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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("Escape Key detected")
                        running = False
                    # if event.key == pygame.K_q:
                        # print("Key q detected") 
                        running = False 
                    
                elif  event.type == pygame.VIDEORESIZE:
                    self._window_resize(event.w, event.h, pygame.RESIZABLE)
                else:
                    pass
                
                
            # self.get_stacks_cards()
            # self.get_stacks_cards_from_server()
            self._window_redraw()
            
            # # place empty cards in the stacks positions
            # self.stacks_layout.render_empty_stacks(self.surface, self.cards)
            
            # # update the window
            # # pygame.display.update()
            # pygame.display.flip()
            
            # delay
            pygame.time.delay(100)
            
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



            # clock.tick(3000)

        self._comm.server_quit()
        pygame.quit()

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







def update_stacks(surface: pygame.Surface):
    #TODO: Implement the update_stacks function
    ...




if __name__ == "__main__":
    game: Game = Game()
    # pygame_init()
    # surface: pygame.Surface = window_init()
    # cards: Cards = Cards(GAME_HEIGHT)
    # stacks_layout: StacksLayout = StacksLayout(cards)
    # stacks_cards: dict[str, list[str]] = player_stacks_init(1)
    # load_card_faces()
    # game_loop(game.surface, game.stacks_layout, game.cards)
    game.game_loop()
