# import pygame module to develop game in python
import pygame

import sys
import random

from tkinter import *
from tkinter import messagebox



# pip3 install mysql-connector
import mysql.connector
# connect python to mysql using mysql-connector
# it need host(hosting mysql .... can be other ip also) , user , password , database name
# we can create database in mysql - workbech it comes with mysql installer for windows
mydb = mysql.connector.connect(host="localhost",user="ganesh",passwd="*********",database="game1")
# for fetching data from database using python we need a cursor  , kind of pointer
mycursor = mydb.cursor()
# after creating cursor every mysql query is executed using execute method
mycursor.execute("select * from user_score")
# display fetched data


# activate the pygame library
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

max_score = mycursor.fetchone()[0]
print("1st time From DB MAX SCORE: " + str(max_score))

WIDTH = 800
HEIGHT = 600

SPEED = 5

# create the display surface object
# of specific dimension..e(X, Y).
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# set the pygame window name
pygame.display.set_caption('Save Player Game '+" Max Score: "+str(max_score))

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
        window = Tk()
        window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
        window.withdraw()

        print(str(current_score) + " " + str(max_score))
        if current_score > max_score:
            print("saving....")
            max_score = current_score
            mycursor.execute("update user_score set score = " + str(current_score) )
            mydb.commit()


        pygame.display.set_caption('Save Player Game ' + " Max Score: " + str(max_score))
        mycursor.execute("select * from user_score")

        max_score = mycursor.fetchone()[0]
        print("Retrived From DB: " + str(max_score))

        if messagebox.askyesno("Question","Want To Start New Game"):
            current_score = 0
            SPEED = 5
            player_position = [WIDTH / 2, HEIGHT - 2 * player_size]

            for idx, enemy_position in enumerate(enemy_list):
                enemy_list.pop(idx)
            window.deiconify()
            window.destroy()
            window.quit()

            enemy_list = [enemy_position]
            #print(enemy_list)
            continue
        else:
            game_over = True
            break

    draw_enemy(enemy_list)

    pygame.draw.rect(screen, (255, 0, 0), (player_position[0],player_position[1], 50, 50))

    clock.tick(30)
    # Draws the surface object to the screen.
    pygame.display.update()
