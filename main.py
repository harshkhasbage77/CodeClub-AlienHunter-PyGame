import math
#from mimetypes import init
#from pickle import TRUE
#from random import Random, random
from random import randint
from tkinter import font
#from telnetlib import PRAGMA_HEARTBEAT
#from tkinter.tix import Tree
#from turtle import Screen, distance
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Creating a Screen/Window
screen = pygame.display.set_mode((800,600))

# Background 
background = pygame.image.load("background.png")

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Alien Hunter")
icon = pygame.image.load("plasma.jpg")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")
playerX = 370 # HALF OF 800 IS 400 BUT AS WE CHOSE IMAGE OF 64 PIXELS SIZE TO CONSIDERING THE SIZE OF IMAGE 370+32 IS APPROX 400 WHICH IS MIDDLE OF SCREEN
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(randint(0, 800)) # First I tried to import whole erntire library  USING : #from random import Random, random BUT it failed...then Harshit suggested to directly import randit USING from random import randint NOW it is working
    enemyY.append(randint(50, 150))
    enemyX_change.append(0.15)
    enemyY_change.append(20)

# Missile

# Ready - You can't see the missile on the screen 
# Fire - The missile is currently moving
missileImg = pygame.image.load("missile.png")
missileX = 0 # First I tried to import whole erntire library  USING : #from random import Random, random BUT it failed...then Harshit suggested to directly import randit USING from random import randint NOW it is working
missileY = 480
missileX_change = 0
missileY_change = 0.5
missile_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 610
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x,y):
    score = font.render("Score : " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER :[", True, (255,255,255))
    screen.blit(over_text, (200, 250))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_missile(x, y):
    global missile_state 
    missile_state = "fire"
    screen.blit(missileImg, (x + 16, y + 10))

'''def isCollision( enemyX, enemyY, missileX, missileY ):
    distance = int(math.sqrt(math.pow(enemyX - missileX, 2) + math.pow(enemyY-missileY,2)))
    if distance < 27:
        #global collision_done
        #collision_done = True
        return True
    else:
        #collision_done = False
        return False'''

def isCollision(enemyX, enemyY, missileX, missileY):
    distance = math.sqrt(math.pow(enemyX - missileX, 2) + (math.pow(enemyY - missileY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True
while running:

    # rgb
    screen.fill((0,0,0))

    # Background Image
    screen.blit(background, (0, 0))

    # playerX += 0.1
    # playerY -= 0.1
    # print(playerX) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is is pressed check whether its right or left
        if event.type == pygame.KEYDOWN: # THIS MEANS PRESSING ANY KEY ON KEYBOARD
            # print("A keystroke is pressed")
            if event.key == pygame.K_LEFT:
                # print("Left arrow is pressed")
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                # print("Right arrow is pressed")
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if missile_state == "ready":
                    missile_Sound = mixer.Sound('laser.wav')
                    missile_Sound.play()
                    # Get the current x cordinate of the spaceship
                    missileX = playerX
                    fire_missile(missileX,missileY)

        if event.type == pygame.KEYUP: # THIS MEANS RELEASING ANY KEY ON KEYBOARD
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                # print("Keystroke has been released")
                playerX_change = 0

    # checking for boundries so that the player doesn't move out
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break    

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], missileX, missileY)
        if collision: 
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            missileY = 480
            missile_state = "ready"
            score_value += 5
            # print(score_value)
            enemyX[i] = randint(0, 736)
            enemyY[i] = randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)    

    # Missile Movement    
    if missileY <= 0:
        missileY = 480
        missile_state = "ready" 

    if missile_state == "fire":
        # missileX = playerX # THIS WILL DEFINITELY GIVE WRONG RESULTS
        fire_missile(missileX,missileY)
        missileY -= missileY_change
        # fire_missile(playerX,playerY) # THIS WAS GIVEN  WRONG RESULTS

    player(playerX,playerY)
    show_score(textX, textY)
    pygame.display.update()

'''
    # Collision
    collision = isCollision(enemyX,enemyY,missileX,missileY)
    if collision: 
        missileY = 480
        missile_state = "ready"
        score += 5
        print(score)
        enemyX = randint(0, 800)
        enemyY = randint(50, 150)
'''