import pygame

GAME_WIDTH: int = 1024
GAME_HEIGHT: int = 768
GAME_ICON: pygame.Surface = pygame.image.load("img/two_backs_256x256.png")

# Initialiasing background colour
FELT_GREEN = (0, 96, 0) # felt dark green colour
FELT_RED = (96, 0, 0)
FELT_BLUE = (0, 0, 96)
YELLOW = (255, 255, 0)

# size of the image files - objective value based on the graphics files used for th game
card_img_height: int = 333
card_img_width: int = 234
card_scale: float = GAME_HEIGHT / 7  # Assuming landscape mode is used
card_game_height: int = int(card_scale)
card_game_width: int = int(card_img_width * card_game_height / card_img_height)


class StackPositions:
    _x: int
    _y: int
    # _name: str

    def __init__(self, x: int, y: int) -> None:
        if  x < 0 or \
            y < 0 or \
            x > (GAME_WIDTH - card_game_width) or\
            y > (GAME_HEIGHT - card_game_height):
            raise ValueError("The stack is not being positioned on the game area")
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x
    
    @property
    def y(self) -> int:
        return self._y

# vertical alignments
OPPONENT_ROW: int = int(card_game_height / 7)

TABLEAU_ROW_1: int = OPPONENT_ROW + card_game_height + int(card_game_height / 7)
TABLEAU_ROW_2: int = TABLEAU_ROW_1 + card_game_height + int(card_game_height / (7 + 7/3))
TABLEAU_ROW_3: int = TABLEAU_ROW_2 + card_game_height + int(card_game_height / (7 + 7/3))
TABLEAU_ROW_4: int = TABLEAU_ROW_3 + card_game_height + int(card_game_height / (7 + 7/3))

FOUNDATION_ROW_1: int = TABLEAU_ROW_1 + int((card_game_height - card_game_width) /2)
FOUNDATION_ROW_2: int = TABLEAU_ROW_2 + int((card_game_height - card_game_width) /2)
FOUNDATION_ROW_3: int = TABLEAU_ROW_3 + int((card_game_height - card_game_width) /2)
FOUNDATION_ROW_4: int = TABLEAU_ROW_4 + int((card_game_height - card_game_width) /2)

PLAYER_ROW: int = TABLEAU_ROW_4 + card_game_height + int(card_game_height / 7)

# horizontal alignments
REMAINDER_OPPONENT_COL: int = int(GAME_WIDTH / 2) - int(card_game_width / 2)
BIN_OPPONENT_COL: int = REMAINDER_OPPONENT_COL - int(card_game_width / 2) - card_game_width
CRAPETTE_OPPONENT_COL: int = REMAINDER_OPPONENT_COL + card_game_width + int(card_game_width / 2)

CRAPETTE_PLAYER_COL: int = BIN_OPPONENT_COL
REMAINDER_PLAYER_COL: int = REMAINDER_OPPONENT_COL
BIN_PLAYER_COL: int = CRAPETTE_OPPONENT_COL

FOUNDATION_PLAYER_COL: int = int(GAME_WIDTH / 2) + int(card_game_width / 4)
TABLEAU_PLAYER_COL: int = int(GAME_WIDTH / 2) + card_game_height + int(card_game_width / 2)
FOUNDATION_OPPONENT_COL: int = int(GAME_WIDTH / 2) - int(card_game_width / 4) - card_game_height
TABLEAU_OPPONENT_COL: int = int(GAME_WIDTH / 2) - card_game_height - int(card_game_width / 2) - card_game_width

# stack_positions: name: (x, y), vertical (true) or horizontal
stacks_positions: dict[str, tuple[int, int, bool]] = {
    "opponent_crapette":    (CRAPETTE_OPPONENT_COL,  OPPONENT_ROW, True),
    "opponent_remainder":   (REMAINDER_OPPONENT_COL, OPPONENT_ROW, True),
    "opponent_bin":         (BIN_OPPONENT_COL,       OPPONENT_ROW, True),

    "opponent_tableau_4":   (TABLEAU_OPPONENT_COL, TABLEAU_ROW_4, True),
    "opponent_tableau_3":   (TABLEAU_OPPONENT_COL, TABLEAU_ROW_3, True),
    "opponent_tableau_2":   (TABLEAU_OPPONENT_COL, TABLEAU_ROW_2, True),
    "opponent_tableau_1":   (TABLEAU_OPPONENT_COL, TABLEAU_ROW_1, True),
    
    "opponent_foundation_4": (FOUNDATION_OPPONENT_COL, FOUNDATION_ROW_4, False),
    "opponent_foundation_3": (FOUNDATION_OPPONENT_COL, FOUNDATION_ROW_3, False),
    "opponent_foundation_2": (FOUNDATION_OPPONENT_COL, FOUNDATION_ROW_2, False),
    "opponent_foundation_1": (FOUNDATION_OPPONENT_COL, FOUNDATION_ROW_1, False),

    "player_foundation_1": (FOUNDATION_PLAYER_COL, FOUNDATION_ROW_4, False),
    "player_foundation_2": (FOUNDATION_PLAYER_COL, FOUNDATION_ROW_3, False),
    "player_foundation_3": (FOUNDATION_PLAYER_COL, FOUNDATION_ROW_2, False),
    "player_foundation_4": (FOUNDATION_PLAYER_COL, FOUNDATION_ROW_1, False),

    "player_tableau_1": (TABLEAU_PLAYER_COL, TABLEAU_ROW_4, True),
    "player_tableau_2": (TABLEAU_PLAYER_COL, TABLEAU_ROW_3, True),
    "player_tableau_3": (TABLEAU_PLAYER_COL, TABLEAU_ROW_2, True),
    "player_tableau_4": (TABLEAU_PLAYER_COL, TABLEAU_ROW_1, True),

    "player_crapette":  (CRAPETTE_PLAYER_COL,  PLAYER_ROW, True),
    "player_remainder": (REMAINDER_PLAYER_COL, PLAYER_ROW, True),
    "player_bin":       (BIN_PLAYER_COL,       PLAYER_ROW, True),
}


card_faces: dict[str, pygame.Surface] = {}
clock: pygame.time

def pygame_init():
    # Initialise pygame
    pygame.init()
    # (numpass, numfail) = pygame.init()
    # print(f"{numpass=}, {numfail=}")

def window_init() -> pygame.Surface:
    # Set up the game window
    surface: pygame.Surface = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT)) #, pygame.RESIZABLE)
    # screen = pygame.display.set_mode()
    # print(f"{screen.get_size()=}")

    # Set title of window
    pygame.display.set_caption("pygame title")

    # Set icon if window
    pygame.display.set_icon(GAME_ICON)

    # color = FELT_GREEN
    # Changing the surface colour
    surface.fill(FELT_GREEN)
    # pygame.display.flip()
    return surface


def load_card_faces():
    import os
    # Get the directory of the script
    card_faces_images_dir = os.path.dirname(os.path.abspath(__file__)) + "/img/card_faces"
    
    # Get all SVG files in the directory
    svg_files = [f for f in os.listdir(card_faces_images_dir) if f.endswith('.svg')]
    for card in svg_files:
        # print(card)
        card_faces[card[0] + card[1]] = pygame.image.load(card_faces_images_dir + "/" + card)

    # print(card_faces.keys)
    # add back_blue, back_red, empty_card
    card_faces["BB"] = pygame.image.load(card_faces_images_dir + "/BB.png")
    card_faces["BR"] = pygame.image.load(card_faces_images_dir + "/BR.png")
    card_faces["EC"] = pygame.image.load(card_faces_images_dir + "/EC.png")
    pygame.Surface.set_colorkey(card_faces["EC"], (255, 255, 255))

    for card in card_faces:
        card_faces[card].convert()
        card_faces[card] = pygame.transform.smoothscale(card_faces[card], (card_game_width, card_game_height))


def place_stacks(surface: pygame.Surface):
    for stack in stacks_positions:
        blit_blank = card_faces["EC"] if stacks_positions[stack][2] \
            else pygame.transform.rotate(card_faces["EC"], 90)
        pygame.Surface.set_colorkey(blit_blank, (255, 255, 255))
        surface.blit(blit_blank, (stacks_positions[stack][0], stacks_positions[stack][1]) )


def game_loop(surface: pygame.Surface):
    # clock = pygame.time.Clock()

    blit_card = card_faces["HQ"]
    blit_card_width = card_faces["HQ"].get_width()
    blit_card_height = card_faces["HQ"].get_height()
    blit_card_angle = 0

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
            else:
                pass
        
        # set background colour
        surface.fill(color)
        # color = FELT_RED if color == FELT_GREEN else FELT_GREEN
        place_stacks(surface)
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
        pygame.display.update()
        pygame.time.delay(100)

        # clock.tick(3000)


    pygame.quit()


if __name__ in "__main__":
    pygame_init()
    surface: pygame.Surface = window_init()
    load_card_faces()
    game_loop(surface)
