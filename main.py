import pygame

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Access a QUIT event and close the window when it is clicked
windowRunning = True
while windowRunning:  # we can access QUIT event when the window is running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Change the boolean to false so that the while loop can stop
            windowRunning = False
