import pygame
import random
import math

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))
# Load background image
backgroundImg = pygame.image.load("images/bg.png")

# Title and Icon
pygame.display.set_caption("Space Invaders")
# 32 Pixel PNG image recommended
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)

# Add the player image and position it on the screen
playerImg = pygame.image.load("images/player.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy image (Now multiple enemies as list)
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("images/enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1.5)
    enemyY_change.append(40)

# Bullet image
# Ready - you can't see the bullet on the screen
# Fire - the bullet is currently moving
bulletImg = pygame.image.load("images/bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 4
bullet_state = "ready"

# Store player score
score = 0


# Function to draw (using blit function) image on the screen
def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, n):
    screen.blit(enemyImg[n], (x, y))


# Checking for boundaries of spaceship so that it does not go out of bound
def playerBoundary():
    global playerX
    global playerY
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # Cater for size of the player image
        playerX = 736


def enemyBoundary():
    global enemyX, enemyY, enemyX_change, bulletY, bullet_state, score

    # Move every enemy in a list
    for n in range(num_of_enemies):
        enemyX[n] += enemyX_change[n]
        if enemyX[n] <= 0:
            enemyX_change[n] = 1.5
            enemyY[n] += enemyY_change[n]
        elif enemyX[n] >= 736:
            enemyX_change[n] = -1.5
            enemyY[n] += enemyY_change[n]

        # Detect collision
        collision = isCollision(enemyX[n], enemyY[n], bulletX, bulletY)
        if collision:  # Reset bullet to starting point and state ready to fire
            bulletY = 480
            bullet_state = "ready"
            score += 1
            # Reset enemy to starting point
            enemyX[n] = random.randint(0, 736)
            enemyY[n] = random.randint(50, 150)

            print("Score: ", score)
        # Display which image
        enemy(enemyX[n], enemyY[n], n)


# Bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def bullet_movement():
    global bulletY
    global bullet_state

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


def isCollision(enemy_x, enemy_y, bullet_x, bullet_y):
    # Using formular from distance of two coordinates in math
    distance = math.sqrt((math.pow((enemy_x - bullet_x), 2)) + (math.pow((enemy_y - bullet_y), 2)))
    if distance < 27:
        return True
    else:
        return False


# Loop of the Game, main logic
windowRunning = True
while windowRunning:  # we can access QUIT event when the window is running
    # Background colour
    screen.fill((0, 0, 0))
    # Add background image
    screen.blit(backgroundImg, (0, 0))

    # Access a QUIT event and close the window when it is clicked
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Change the boolean to false so that the while loop can stop
            windowRunning = False

        # If keystroke is pressed check whether it is left or right keystroke
        if event.type == pygame.KEYDOWN:  # if any keystroke is pressed down
            if event.key == pygame.K_LEFT:  # then if the key is LEFT arrow, move player to Left by 0.1
                playerX_change = -2.5
            if event.key == pygame.K_RIGHT:  # then if the key is RIGHT arrow, move player to Right by 0.1
                playerX_change = 2.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # Get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:  # if any keystroke pressed is released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # When either Left or Right key released, stop the X coordinate and maintain that position
                playerX_change = 0

    # Player movement
    playerX += playerX_change  # Change the X coordinate
    playerBoundary()  # Apply boundaries accordingly
    # Enemy movement
    enemyBoundary()
    # Bullet movement
    bullet_movement()

    player(playerX, playerY)

    pygame.display.update()

    # Ended at 1:34 minutes
