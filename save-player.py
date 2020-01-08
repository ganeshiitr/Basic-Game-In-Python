import pygame
import sys
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SPEED = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Save the player: Ganesh')

current_score = 0

clock = pygame.time.Clock()

player_size = 50
player_position = [WIDTH / 2 , HEIGHT - 2 * player_size]

enemy_size = 50
enemy_position = [100, -50]
enemy_list = [enemy_position]

FPS = 30

# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)


def update_speed():
    global SPEED
    if current_score < 30:
        SPEED = 5
    elif current_score < 60:
        SPEED = 10
    elif current_score < 90:
        SPEED = 15
    else:
        SPEED = 20


def update_score():
    global current_score
    current_score = current_score + 1
    update_speed()


def add_enemy(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, WIDTH - enemy_size)
        y_pos = -50
        enemy_list.append([x_pos,y_pos])

def update_enemy_position(enemy_list):
    for idx,enemy_position in enumerate(enemy_list):
        if enemy_position[1] >= -50 and enemy_position[1] < HEIGHT:
            enemy_position[1] = enemy_position[1] + SPEED
        else:
            enemy_list.pop(idx)
            update_score()

def collision_check(enemy_list, player_position):
    for enemy_position in enemy_list:
        if detect_collision(player_position,enemy_position):
            return True
    return False


def draw_enemy(enemy_list):
    for enemy_position in enemy_list:
        pygame.draw.rect(screen, BLUE, (enemy_position[0], enemy_position[1], enemy_size, enemy_size))

def detect_collision(player_position,enemy_position):
    p_x = player_position[0]
    p_y = player_position[1]

    e_x = enemy_position[0]
    e_y = enemy_position[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + player_size)):
        if(e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + player_size)):
            return True

    return False

def message_to_screen(text, cx, cy, fg_color = WHITE, bg_color = None):
    # create a text suface object,
    # on which text is drawn on it.
    if bg_color == None:
        text = font.render(text , True, fg_color)
    else:
        text = font.render(text , True, fg_color, bg_color)
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
    # set the center of the rectangular object.
    textRect.center = (cx, cy)

    # copying the text surface object
    # to the display surface/screen object
    # at the center coordinate.
    screen.blit(text, textRect)

def game_loop():
    global current_score

    x = player_position[0]
    y = player_position[1]
    x_change = 0

    enemy_position = [100, -50]
    enemy_list = [enemy_position]

    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change

        screen.fill(BLACK)

        add_enemy(enemy_list)
        update_enemy_position(enemy_list)

        message_to_screen("Score: " + str(current_score), WIDTH - 2 * player_size , HEIGHT - 2 * player_size, GREEN)
        #print(current_score)

        if collision_check(enemy_list, [x, y]):
            message_to_screen("You lost. Press ENTER to restart.", WIDTH / 2, HEIGHT / 2 - 16)
            pygame.display.update()

            restart_f = False
            while not restart_f:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            restart_f = True

                clock.tick(10)

            current_score = 0
            SPEED = 5
            [x, y] = [WIDTH / 2, HEIGHT - 2 * player_size]
            enemy_list = [enemy_position]
            x_change = 0
            pygame.display.update()
            continue

        draw_enemy(enemy_list)

        pygame.draw.rect(screen, RED, (x, y, player_size, player_size))

        pygame.display.update()
        clock.tick(FPS)

game_loop()