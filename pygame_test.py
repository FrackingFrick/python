"""
Testing out Pygame library
"""

import pygame

# Initialise Pygame
pygame.init()

# Screen size
width, height = 800, 600

# Create the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame intro")

# Change the colour of the screen
screen.fill((255, 255, 255))

# Draw a line
pygame.draw.line(screen, (0, 255, 0), [width / 2, 0], [width / 2, height / 2], 10)

# Draw a circle
pygame.draw.circle(screen, (0, 0, 0), [width / 2, height / 2], 25)

# Game loop
running = True
while running:
    # Handle all the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                screen.fill((255, 0, 0))
            if event.key == pygame.K_y:
                pygame.draw.circle(screen, (255, 200, 12), [width / 2, height / 2], 25)
                pygame.display.update()
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                screen.fill((255, 255, 255))
       

    # Update the positions and velocities of the objects
    # ....

    # Update the screen
    # pygame.draw.line(screen, (0, 255, 0), [width / 2, 0], [width / 2, height / 2], 10)
    # pygame.draw.circle(screen, (0, 0, 0), [width / 2, height / 2], 25)
    pygame.display.update()