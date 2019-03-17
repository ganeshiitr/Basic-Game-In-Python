import pygame
import sys
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

SPEED = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Save Player : Ganesh')

game_over = False
current_score = 0

clock = pygame.time.Clock()

player_size = 50
player_position = [WIDTH / 2 , HEIGHT - 2 * player_size]

enemy_size = 50
enemy_position = [100,0]
enemy_list = [enemy_position]

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
        x_pos = random.randint(0,WIDTH-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos,y_pos])

def update_enemy_position(enemy_list):
    for idx,enemy_position in enumerate(enemy_list):
        if enemy_position[1] >= 0 and enemy_position[1] < HEIGHT:
            enemy_position[1] = enemy_position[1]+SPEED
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
        pygame.draw.rect(screen, (0, 0, 255), (enemy_position[0], enemy_position[1], 50, 50))

def detect_collision(player_position,enemy_position):
    p_x = player_position[0]
    p_y = player_position[1]

    e_x = enemy_position[0]
    e_y = enemy_position[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + player_size)):
        if(e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + player_size)):
            return True
    return  False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            x = player_position[0]
            y = player_position[1]

            if event.key == pygame.K_LEFT:
                x = x - player_size
            if event.key == pygame.K_RIGHT:
                x = x + player_size
            player_position = [x,y]

    screen.fill((0, 0, 0))

    add_enemy(enemy_list)
    update_enemy_position(enemy_list)

    # create a text suface object,
    # on which text is drawn on it.
    text = font.render("Score: " + str(current_score) , True, (0, 255, 0), (0, 0, 255))

    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
    # set the center of the rectangular object.
    textRect.center = (WIDTH - 2 * player_size , HEIGHT - 2 * player_size)

    # copying the text surface object
    # to the display surface/screen object
    # at the center coordinate.
    screen.blit(text, textRect)

    #print(current_score)

    if collision_check(enemy_list,player_position):
        game_over = True
        break
    draw_enemy(enemy_list)

    pygame.draw.rect(screen, (255, 0, 0), (player_position[0],player_position[1], 50, 50))

    clock.tick(30)
    pygame.display.update()
