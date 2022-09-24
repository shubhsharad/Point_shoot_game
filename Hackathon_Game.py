import pygame, random, sys, os
from pygame.locals import *

pygame.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,128)
TURQ = (0,255,255)
GRAY = (224,224,224)
PURPLE = (102,0,51)
MAGENTA = (102,0,204)
WINDOWHEIGHT = 750
WINDOWWIDTH = 1000
gameDisplay = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
FONT = pygame.font.SysFont(None, 48)
SPACE = pygame.image.load( 'bg.png')
SPACE = pygame.transform.scale(SPACE, (WINDOWWIDTH, WINDOWHEIGHT))
SPACE2 = pygame.image.load( 'gameoverbg.png')
SPACE2 = pygame.transform.scale(SPACE2, (WINDOWWIDTH, WINDOWHEIGHT))

bg_img = pygame.image.load('mainbg.png')
bg_img = pygame.transform.scale(bg_img, (WINDOWWIDTH, WINDOWHEIGHT))



def terminate():
    pygame.quit()
    sys.exit()

def Menu():
    timer = 0
    color = BLUE
    switch = False
    while True:
        gameDisplay.blit(SPACE, (0,0))
        difficultyRects = []
        difficultyRects.append(pygame.Rect(5, 450, 240, 100))
        difficultyRects.append(pygame.Rect(255, 450, 240, 100))
        difficultyRects.append(pygame.Rect(505, 450, 240, 100))
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
            if event.type == MOUSEBUTTONDOWN:
                if difficultyRects[0].collidepoint(pygame.mouse.get_pos()):
                    game("easy")
                if difficultyRects[1].collidepoint(pygame.mouse.get_pos()):
                    game("medium")
                if difficultyRects[2].collidepoint(pygame.mouse.get_pos()):
                    game("hard")
        for rect in difficultyRects:
            pygame.draw.rect(windowSurface, PURPLE, rect)
        drawText("Pick a difficulty", windowSurface, 90, 150, pygame.font.SysFont(None, 112), color)
        drawText("Easy", windowSurface, 83, 485, FONT , GRAY)
        drawText("Medium", windowSurface, 312, 485,FONT , GRAY)
        drawText("Hard", windowSurface, 580, 485,FONT , GRAY)
        mainClock.tick(50)
        timer += 1
        if timer % 100 == 0:
            color = BLUE
        elif timer % 50 == 0:
            color = MAGENTA
        pygame.display.update()

def drawText(text, surface, x, y, font = FONT, color = TURQ):
    textObject = font.render(text, 1, color)
    textRect = textObject.get_rect()
    textRect.topleft = (x,y)
    surface.blit(textObject, textRect)

def gameOver(totalShots, hitShots, difficulty, score):
    pygame.mouse.set_visible(True)
    if totalShots != 0 and hitShots != 0:
        accuracy = round(hitShots/totalShots * 100)
    else:
        accuracy = 0
    gameDisplay.blit(SPACE2, (0,0))
    drawText("GAME OVER", windowSurface, 330, 305, pygame.font.SysFont(None, 72, True),PURPLE)
    drawText("Click anywhere to restart", windowSurface, 300, 350,FONT,BLACK)
    drawText("Accuracy: " + str(accuracy) + "%", windowSurface, 375, 385,FONT,PURPLE)
    drawText("Score: " + str(score), windowSurface, 375, 420,FONT,PURPLE)
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONDOWN:
                windowSurface.fill(BLACK)
                Menu()
            if event.type == KEYDOWN:
                terminate()

def populateConfig(difficulty):
    global targetImage
    targetImage = pygame.image.load("ufo-removebg.png")
    config = {}
    if(difficulty == "easy"):
        difficultyFile = open("easy.txt", "r")
    elif(difficulty == "medium"):
        difficultyFile = open("medium.txt", "r")
    elif(difficulty == "hard"):
        difficultyFile = open("hard.txt", "r")
    for line in difficultyFile:
        splitLine = line.split(":")
        splitLine[1] = splitLine[1].strip("\n")
        config[splitLine[0]] = int(splitLine[1])
    targetImage = pygame.transform.scale(targetImage, (config["enemySize"],config["enemySize"]))
    difficultyFile.close()
    return config

mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
pygame.display.set_caption("SHOOT")

shootSound = pygame.mixer.Sound("laser_gun.wav")
hitSound = pygame.mixer.Sound("spacehit.wav")
shootSound.set_volume(0.07)
hitSound.set_volume(0.02)


enemies = []
width = 750 

def game(difficulty):
    i = 0
    config = populateConfig(difficulty)
    
    pygame.mouse.set_visible(False)
    
    mouseY = (round(WINDOWHEIGHT / 2))
    mouseX = (round(WINDOWWIDTH / 2))
    
    tickCounter = 0
    enemies = []
    amountOfEnemies = 0
    score = 0
    FPS = 75
    hitShots = 0
    totalShots = 0
    STARTINGTIME = config.get("time")
    CIRCLERADIUS = 150
    while True:
        if(config.get("time") <= 0):
            gameOver(totalShots, hitShots, difficulty, score)
        tickCounter += 1
        if(tickCounter % FPS == 0):
            config["time"] -= 1
        
        gameDisplay.fill((0,0,0))
        gameDisplay.blit(bg_img,(i,0))
        gameDisplay.blit(bg_img,(width+i,0))
        
        if i == (-width):
            i = 0
        i -= 1
        

        if (amountOfEnemies == 0):
            config["time"] = STARTINGTIME
            while(amountOfEnemies != config.get("maxAmountOfEnemies")):
                enemies.append(pygame.Rect((random.randint(0,WINDOWWIDTH - config.get("enemySize"))),
                                           (random.randint(0,WINDOWHEIGHT - config.get("enemySize"))),
                                           config.get("enemySize"), config.get("enemySize")))
                if enemies[amountOfEnemies].topleft[0] < 135 and enemies[amountOfEnemies].topleft[1] < 65:
                    enemies.pop(amountOfEnemies)
                else:
                    amountOfEnemies += 1
        for event in pygame.event.get():
                       
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                pass
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
            if event.type == MOUSEMOTION:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
            if event.type == MOUSEBUTTONDOWN:
                pygame.mixer.Channel(0).play(shootSound)
                totalShots += 1
                for enemy in enemies[:]:
                    if (mouseX >= enemy.topleft[0] and mouseX <= enemy.bottomright[0])\
                       and (mouseY >= enemy.topleft[1] and mouseY <= enemy.bottomright[1]):
                        pygame.mixer.Channel(1).play(hitSound)
                        enemies.remove(enemy)
                        amountOfEnemies -= 1
                        score += 1
                        hitShots += 1
                
                        
                                           
        
        for enemy in enemies:
            windowSurface.blit(targetImage, enemy)
        
        pygame.draw.line(windowSurface, WHITE, (mouseX, mouseY + 15),
                        (mouseX, mouseY - 15), 2)
        pygame.draw.line(windowSurface, WHITE, (mouseX + 15, mouseY),
                        (mouseX - 15, mouseY), 2)
        drawText("Time: " + str(config.get("time")), windowSurface, 8,8)
        drawText("Score: " + str(score), windowSurface, 8,38)
        pygame.display.update()
        mainClock.tick(FPS)
Menu()