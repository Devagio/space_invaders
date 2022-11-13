import pygame
import random
from pygame import mixer


# Initialize the pygame
pygame.init()


# Create the screen
width = 800
height = 600
screen = pygame.display.set_mode((width, height))


# Background
background = pygame.image.load("background.png")


# Background music
mixer.music.load("music.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.2)


# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)


# Player
player_image = pygame.image.load('battleship.png')
player_image_size = 64
player_x = (width - player_image_size) / 2
player_y = height - player_image_size
player_x_change = 0
speed = 3


def player(x, y):
    screen.blit(player_image, (x, y))


# Enemy
enemy_image = pygame.image.load("ufo.png")
enemy_x = []
enemy_y = []
enemy_image_size = 64
enemy_x_speed = []
enemy_y_change = enemy_image_size
enemy_num = 1
enemy_mod_speed = 3
for i in range(enemy_num):
    enemy_x.append(random.randint(0, width - enemy_image_size))
    enemy_y.append(random.randint(0, 2 * enemy_image_size))
    enemy_x_speed.append(enemy_mod_speed * random.choice([1, -1]))


def enemy(x, y):
    screen.blit(enemy_image, (x, y))


# Bullet
bullet_image = pygame.image.load('bullet.png')
bullet_image_size = 32
bullet_x = player_x + (player_image_size - bullet_image_size) / 2
bullet_y = player_y
bullet_y_speed = -10
bullet_state = "ready"


def bullet(x, y):
    screen.blit(bullet_image, (x, y))


def is_collision(e_x, e_y, b_x, b_y):
    global enemy_image_size
    global bullet_image_size
    if (e_y + enemy_image_size > b_y) and (e_y < b_y):
        if abs(b_x + bullet_image_size / 2 - e_x - enemy_image_size / 2) < enemy_image_size / 2:
            return True
    return False


# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Game over
go_font = pygame.font.Font("freesansbold.ttf", 64)
go_text_x = 200
go_text_y = 250
go = False


def game_over(x, y):
    go_message = go_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(go_message, (x, y))


# Game Loop
running = True
left_key = False
right_key = False
while running:
    for event in pygame.event.get():
        # Quit event
        if event.type == pygame.QUIT:
            running = False

        # Player motion via key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_key = True
            if event.key == pygame.K_RIGHT:
                right_key = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_key = False
            if event.key == pygame.K_RIGHT:
                right_key = False

        if left_key and right_key:
            player_x_change = 0
        elif left_key:
            player_x_change = -speed
        elif right_key:
            player_x_change = speed
        else:
            player_x_change = 0

        # Bullet trigger
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_x = player_x + (player_image_size - bullet_image_size) / 2
                bullet(bullet_x, bullet_y)
                bullet_state = "fire"
                mixer.Sound('fire.wav').play()

    # background in RGB
    screen.fill((0, 0, 100))
    # background in RGB
    screen.blit(background, (0, 0))

    # Collision Detection
    for i in range(len(enemy_x)):
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_state = "ready"
            bullet_y = player_y
            score_value = score_value + 1
            enemy_x.pop(i)
            enemy_y.pop(i)
            enemy_x_speed.pop(i)
            mixer.Sound('explosion.wav').play()
            break

    if len(enemy_x) == 0:
        enemy_num = enemy_num + 1
        enemy_mod_speed = enemy_mod_speed + 0.5
        for i in range(enemy_num):
            enemy_x.append(random.randint(0, width - enemy_image_size))
            enemy_y.append(random.randint(0, 2 * enemy_image_size))
            enemy_x_speed.append(enemy_mod_speed * random.choice([1, -1]))

    # player render
    player_x = player_x + player_x_change
    if player_x < 0 or player_x > width - player_image_size:
        player_x = player_x - player_x_change
    player(player_x, player_y)

    # enemies render
    for i in range(len(enemy_x)):
        if enemy_x[i] <= 0 or enemy_x[i] >= width - enemy_image_size:
            enemy_x_speed[i] = enemy_x_speed[i] * -1
            enemy_y[i] = enemy_y[i] + enemy_y_change
        enemy_x[i] = enemy_x[i] + enemy_x_speed[i]
        enemy(enemy_x[i], enemy_y[i])

    # bullet render
    if bullet_state == "fire":
        bullet_y = bullet_y + bullet_y_speed
        bullet(bullet_x, bullet_y)
        if bullet_y < 0:
            bullet_state = "ready"
            bullet_y = player_y

    # Game over
    for i in range(len(enemy_x)):
        if enemy_y[i] + enemy_image_size > player_y and abs(enemy_x[i] - player_x) < enemy_image_size:
            for j in range(len(enemy_x)):
                enemy_y[j] = height
                go = True
    if go:
        game_over(go_text_x, go_text_y)

    # update screen
    show_score(text_x, text_y)
    pygame.display.update()
