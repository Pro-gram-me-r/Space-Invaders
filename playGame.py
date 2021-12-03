import pygame
import random
import math
from pygame import mixer

# Startup
pygame.init()

# creating the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('universe.jpg')

# Background Music
mixer.music.load('background.mp3')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")

icon = pygame.image.load('alien.jpg')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 320
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 725))
    enemyY.append(random.randint(50, 250))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('Bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.8
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Game over screen
over_font = pygame.font.Font('freesansbold.ttf', 64)


def shoe_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render('GAME OVER ', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 24, y - 16))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('shooting.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # PLAYER Boundaries
    playerX += playerX_change

    if playerX <= -0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Game Over
    for i in range(num_of_enemies):
        if enemyY[i] > 408:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        # Enemy Movement
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= -0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 10
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 250)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Boom
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    shoe_score(text_x, text_y)
    pygame.display.update()
