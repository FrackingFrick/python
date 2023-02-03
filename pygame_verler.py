"""
Motion of a mass visualised using Pygame
"""

import pygame

# Physical parameters
g = 10
k = 1
m = 1
L = 100

# Initialise Pygame
pygame.init()

# Screen size
width, height = 400, 300

# Create the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame intro")

# Create a clock
FPS = 60
clock = pygame.time.Clock()

# Initial values
x_0 = width / 2
y_0 = height / 2
v_x_0 = 0
v_y_0 = 0

# Time step
dt = 0.01

# Initialise the variables
x = x_0
y = y_0
v_x = v_x_0
v_y = v_y_0

# Change the colour of the screen
screen.fill((255, 255, 255))

# Draw a circle
pygame.draw.circle(screen, (0, 0, 0), [width / 2, height / 2], 25)

# Draw a line
pygame.draw.line(screen, (0, 255, 0), [width / 2, 0], [width / 2, height / 2], 10)

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
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                screen.fill((255, 255, 255))

    # Update the positions and velocities of the objects
    a_x = 0
    a_y = g - k/m * (y - L) - 0.2 * v_y

    x = x + dt * v_x + 0.5 * dt**2 * a_x
    v_x = v_x + dt * a_x
    y = y + dt * v_y + 0.5 * dt**2 * a_y
    v_y = v_y + dt * a_y
    a_y_new = g - k/m * (y - L) - 0.2 * v_y
    v_y = v_y + dt * (a_y + a_y_new) / 2

    # a = g - k/m * (x - L) - 0.2 * v
    # x_new = x + dt * v + 0.5 * dt**2 * a
    # v_new = v + dt * a
    # a_new = g - k/m * (x_new - L) - 0.2 * v_new
    # v_new = v + dt * (a + a_new) / 2
    # t_new = t + dt

    # Update the screen
    screen.fill((255, 255, 255))
    pygame.draw.line(screen, (0, 255, 0), [width / 2, 0], [x, y], 10)
    pygame.draw.circle(screen, (0, 0, 0), [x, y], 25)
    pygame.display.update()
    clock.tick(FPS)