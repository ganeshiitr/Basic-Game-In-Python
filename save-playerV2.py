# import pygame module to develop game in python
import pygame

import sys
import random

try:
    from tkinter import *
    from tkinter import messagebox
except:
    from Tkinter import *
    import tkMessageBox as messagebox

# activate the pygame library
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SPEED = 5

# create the display surface object
# of specific dimension..e(X, Y).
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# set the pygame window name
pygame.display.set_caption('Save Player : Ganesh')

current_score = 0

clock = pygame.time.Clock()

player_size = 50
player_position = [WIDTH / 2 , HEIGHT - 2 * player_size]

enemy_size = 50

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
        enemy_list.append([x_pos, y_pos])

def update_enemy_position(enemy_list):
    for idx,enemy_position in enumerate(enemy_list):
        if enemy_position[1] >= -50 and enemy_position[1] < HEIGHT:
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

        # create a text suface object,
        # on which text is drawn on it.
        text = font.render("Score: " + str(current_score) , True, GREEN, BLUE)

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

        if collision_check(enemy_list, [x, y]):
            window = Tk()
            window.withdraw()

            if messagebox.askyesno("You lost","Want to start new game?"):
                current_score = 0
                SPEED = 5
                [x, y] = [WIDTH / 2, HEIGHT - 2 * player_size]

                '''for idx, enemy_pos in enumerate(enemy_list):
                    print idx, enemy_pos
                    enemy_list.pop(idx)'''

                del enemy_list[:]

                window.destroy()
                window.quit()

                enemy_list = [enemy_position]
                #print(enemy_list)
                continue
            else:
                game_over = True
                break

        draw_enemy(enemy_list)

        pygame.draw.rect(screen, RED, (x, y, player_size, player_size))

        clock.tick(30)
        # Draws the surface object to the screen.
        pygame.display.update()

game_loop()