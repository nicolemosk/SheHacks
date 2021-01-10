import pygame

width = 800
height = 600
name = "Game"
bg_colour = (0,0,0)

pygame.init()

screen = pygame.display.set_mode((width,height))

pygame.display.set_caption(name)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(bg_colour)
    pygame.display.update()