import math
import random
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Aliens")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

background = pygame.image.load('background.jpg')
playerImg = pygame.image.load('player.png')
bulletImg = pygame.image.load('bullet.png')
enemyImg = pygame.image.load('enemy.png')
font = pygame.font.Font('VeniteAdoremusStraight-Yzo6v.ttf', 64)

clock = pygame.time.Clock()
FPS = 60

playerX = 370
playerY = 480
playerX_change = 0

bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

num_of_enemies = 6
enemies = []

for i in range(num_of_enemies):
    enemies.append({
        'x': random.randint(0, 736),
        'y': random.randint(50, 150),
        'x_change': 4,
        'y_change': 40
    })

score_value = 0

textX = 10
textY = 10

in_menu = True
selected_option = "Start"

white = (255, 255, 255)
gray = (192, 192, 192)


def show_menu():

    start_text = font.render("Start", True, white)
    exit_text = font.render("Exit", True, white)

    start_text_rect = start_text.get_rect(center=(400, 250))
    exit_text_rect = exit_text.get_rect(center=(400, 350))

    screen.blit(start_text, start_text_rect)
    screen.blit(exit_text, exit_text_rect)

    if selected_option == "Start":
        pygame.draw.rect(screen, gray, start_text_rect, 5)
    elif selected_option == "Exit":
        pygame.draw.rect(screen, gray, exit_text_rect, 5)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, white)
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy_spawn(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + (math.pow(enemy_y - bullet_y, 2)))
    return distance < 27


running = True
while running:

    clock.tick(FPS)

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if in_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = "Exit"
                elif event.key == pygame.K_UP:
                    selected_option = "Start"
                elif event.key == pygame.K_RETURN:
                    if selected_option == "Start":
                        in_menu = False
                    elif selected_option == "Exit":
                        running = False
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                elif event.key == pygame.K_RIGHT:
                    playerX_change = 5
                elif event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

    if in_menu:
        show_menu()
    else:
        playerX += playerX_change
        playerX = max(0, min(playerX, 736))

        for enemy in enemies:
            enemy['x'] += enemy['x_change']
            if enemy['x'] <= 0 or enemy['x'] >= 736:
                enemy['x_change'] = -enemy['x_change']
                enemy['y'] += enemy['y_change']

            if is_collision(enemy['x'], enemy['y'], playerX, playerY):
                in_menu = True
                playerX = 370
                playerY = 480
                score_value = 0

            if is_collision(enemy['x'], enemy['y'], bulletX, bulletY):
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemies.remove(enemy)
                enemies.append({
                    'x': random.randint(0, 736),
                    'y': random.randint(50, 150),
                    'x_change': 4,
                    'y_change': 40
                })

            if bulletY <= 0:
                bulletY = 480
                bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        for enemy in enemies:
            enemy_spawn(enemy['x'], enemy['y'])
        show_score(textX, textY)

    pygame.display.flip()

pygame.quit()
