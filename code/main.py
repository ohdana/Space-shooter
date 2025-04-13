import pygame
from random import randint
from os.path import join

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True

# plain surface
surf = pygame.Surface((100, 200))
surf.fill('orange')
x = 100
n_of_stars = 20

# importing an image
player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
star_positions = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for i in range(n_of_stars)]

while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw the game
    display_surface.fill('darkgray')
    x += 0.1

    for i in range(n_of_stars):
        star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
        display_surface.blit(star_surf, star_positions[i])

    display_surface.blit(player_surf, (x,150))
    pygame.display.update()
pygame.quit()
