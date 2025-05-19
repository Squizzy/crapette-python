import pygame


# Initialise pygame
pygame.init()
# (numpass, numfail) = pygame.init()
# print(f"{numpass=}, {numfail=}")

# Set up the game window
screen = pygame.display.set_mode((400,300))
# screen = pygame.display.set_mode()
# print(f"{screen.get_size()=}")
pygame.display.set_caption("Hello Pygame caption")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()