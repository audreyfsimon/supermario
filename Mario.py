from cmu_112_graphics import *
import random, string, math, time, copy

from cmu_112_graphics import *
import random
from dataclasses import make_dataclass
import pygame


#################################################
# Helper functions
#################################################

# Citation - Taken from 15-112 Website: 
# https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#dimensions

def make2dList(rows, cols, placement):
    return [ ([placement] * cols) for row in range(rows) ]

# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#caching\
# PhotoImages

def getCachedImage(app,image):
    if ('cachedPhotoImage' not in image.__dict__):
        image.cachedPhotoImage = ImageTk.PhotoImage(image)
    return image.cachedPhotoImage

#################################################
# Main App
#################################################

def gameDimensions():
    rows = 18
    cols = 50
    cellSize = 40
    margin = 8
    return rows,cols,cellSize,margin

def playMario():
    rows,cols,cellSize,margin = gameDimensions()
    width = 2*margin+cellSize*cols//2
    height = 2*margin+cellSize*rows
    runApp(width=width, height=height)

#################################################
# Music and Sound Effects
#################################################
# CITATIONS
# jumpSound: https://www.mariomayhem.com/downloads/sounds/NSMBWiiSoundEffects/
#   nsmbwiiClassicSmallJump.wav
# themeSong: https://vgmsite.com/soundtracks/super-mario-bros/khbnvkqp/01%20-%
#   20Super%20Mario%20Bros.mp3
# stompOnGoomba: https://www.mariomayhem.com/downloads/sounds/NSMBWiiSound
#   Effects/nsmbwiiStompMicroGoomba.wav
# killMario: http://www.mediafire.com/file/y0tg2b5dht3git4/Mario_Death_Sound_
#   Effect.mp3/file

pygame.mixer.init()
jumpSound = pygame.mixer.Sound('jump.wav')
stompGoomba = pygame.mixer.Sound('killGoomba.wav')
killMario = pygame.mixer.Sound('marioDeath.mp3')
themeSong = pygame.mixer.music.load('themesong.mp3')

#################################################
# Terrain Generation
#################################################

def drawFloor(rows,cols,terrain,level):
    slant = [[14,1,1,1,15],[0,14,1,15,0]]
    slant1 = [14,1,1,1,1,15]
    slant2 = [[14,1,1,1,1,15],[0,14,1,1,15,0]]
    if level == 0:
        for row in range(len(terrain)-3,len(terrain)):
            for col in range(len(terrain[row])):
                terrain[row][col]=1
        randCol = random.randint(col//2,col-3)
        for row in range(3):
            for col in range(2):
                terrain[row+15][col+randCol] = 0
    else:
        for row in range(len(terrain)-3,len(terrain)):
            for col in range(len(terrain[row])):
                terrain[row][col]=1
        randCol = random.randint(col//2,col-3)
        for row in range(3):
            for col in range(2):
                terrain[row+15][col+randCol] = 0

def drawHoles(rows,cols,terrain,level):
    hole1 = [[0,0],[0,0],[0,0]]
    hole2 = [[0,0,0],[0,0,0],[0,0,0]]
    obj = random.choice([hole1,hole2])
    if level == 0 or cols<=25 or cols<2:
        return
    elif level%3!=0 and level<2:
        return
    else:
        if cols<49:
            for row in range(len(obj)):
                for col in range(len(obj[0])):
                    terrain[17-row][cols+col] = 0
        return drawHoles(rows,cols-random.randint(4,7),terrain,level)

def drawMountain(rows,cols,terrain,level):
    if level==0:
        return
    slant = [[14,1,1,1,15],[0,14,1,15,0]]
    slant1 = [[14,1,1,1,1,15]]
    slant2 = [[14,1,1,1,1,15],[0,14,1,1,15,0]] 
    slant3 = [[14,1,15]] 
    slant4 = [[14,1,1,15]]
    obj = random.choice([slant,slant1,slant2,slant3])
    if level == 1:
        change = random.randint(4,6)
    else:
        change = 1
        obj = random.choice([slant,slant2])
    if cols < 0:
        return
    else:
        if cols<44:
            allLegal = 0
            for row in range(len(obj)):
                for col in range(len(obj[0])):
                    if blockisLegal(terrain,14-row,cols+col,'hill'):
                        allLegal += 1
            if allLegal == len(obj)*len(obj[0]):
                for num in range(len(obj)):
                    for col in range(len(obj[0])):
                        terrain[14-num][cols+col]=obj[num][col]
        return drawMountain(rows,cols-change,terrain,level)

def drawBricks(rows,cols,terrain,level):
    block = random.randint(cols//4+1,cols//4+4)
    if level == 0:
        for col in range(random.randint(3,5)):
            terrain[rows-7][block+col]=2
        for col in range(random.randint(2,4)):
            terrain[rows-11][block+col+2]=2
        block = random.randint(cols//(2)+1,cols//(2)+4)
        for col in range(random.randint(3,5)):
            terrain[rows-7][block+col]=2
        for col in range(random.randint(2,4)):
            terrain[rows-11][block+col+2]=2
        block = random.randint(cols//(4/3)+1,cols//(4/3)+4)
        for col in range(random.randint(3,5)):
            terrain[rows-7][block+col]=2
        for col in range(random.randint(2,4)):
            terrain[rows-11][block+col+2]=2
    else:
        block = random.randint(cols//8+1,cols//8+4)
        for col in range(random.randint(3,5)):
            terrain[rows-7][block+col]=2
        for col in range(random.randint(2,4)):
            terrain[rows-11][block+col+2]=2
        block = random.randint(cols//4+1,cols//4+4)
        for col in range(random.randint(3,5)):
            terrain[rows-7][block+col]=2
        for col in range(random.randint(2,4)):
            terrain[rows-11][block+col+2]=2
        block = random.randint(cols//(2)+1,cols//(2)+4)
        for col in range(random.randint(3,5)):
            terrain[rows-7][block+col]=2
        for col in range(random.randint(2,4)):
            terrain[rows-11][block+col+2]=2
        block = random.randint(cols//(4/3)+1,cols//(4/3)+4)
        for col in range(random.randint(3,5)):
            terrain[rows-7][block+col]=2
        for col in range(random.randint(2,4)):
            terrain[rows-11][block+col+2]=2

def drawClouds(rows,cols,terrain):
    for boardChunk in range(8):
        cloudRow = random.randint(2,3)
        for col in range(1,(random.randint(2,3))):
            terrain[cloudRow][boardChunk*cols//8+col]=3

def drawTube(rows,cols,terrain,level):
    tube1 = [[10, 11,],[12,13]]
    tube2 = [[10,11],[10,11],[12,13]]
    tube3 = [[10,11],[10,11],[10,11],[12,13]]
    if level <=1:
        obj = random.choice([tube1,tube2])
    else:
        obj = random.choice([tube2,tube3])
    if cols < 2:
        return
    elif level == 0 and cols<=25:
        return
    else:
        if cols<49:
            allLegal = 0
            for row in range(len(obj)):
                for col in range(len(obj[0])):
                    if blockisLegal(terrain,14-row,cols+col,'tube'):
                        allLegal += 1
            if allLegal == len(obj)*len(obj[0]):
                for row in range(len(obj)):
                    for col in range(len(obj[0])):
                        terrain[14-row][cols+col] = obj[row][col]
        return drawTube(rows,cols-random.randint(3,7),terrain,level)
                
def blockisLegal(terrain,row,col,obj):
    if terrain[row][col] in [0,3,5,6,7,8,9] and terrain[row][col-1] in \
        [0,3,5,6,7,8,9] and terrain[row][col+1] in [0,3,5,6,7,8,9] and \
        terrain[15][col]==1:
        if obj == 'tube':
            if terrain[row-1][col] ==0 and \
                terrain[row-2][col] ==0 and\
                terrain[row-1][col-1] ==0 and \
                terrain[row-1][col+1] ==0:
                return True
            else:
                return False
        return True
    return False

def drawHill(rows,cols,terrain):
    hill1 = [[ 4, 4, 4,4 ],[ 4, 4, 4,4 ]]## extra 4
    hill2 = [[4,4,4,4,4],[4,4,4,4,4],[4,4,4,4,4]]
    bush1 = [[4,4,4]]
    bush2 = [[4,4,4,4]]
    bush3 = [[4,4,4,4,4]]
    hill1num = 5
    hill2num = 6
    bush1num = 7
    bush2num = 8
    bush3num = 9
    obj = random.choice([hill1,hill1,hill2,bush1,bush2,bush3])
    if cols < 0:
        return
    else:
        if cols<44:
            allLegal = 0
            for row in range(len(obj)):
                for col in range(len(obj[0])):
                    if blockisLegal(terrain,14-row,cols+col,'hill'):
                        allLegal += 1
            if allLegal == len(obj)*len(obj[0]):
                if obj == hill1:
                    terrain[14][cols+len(obj)//2] = hill1num
                elif obj == hill2:
                    terrain[14][cols+len(obj)//2] = hill2num
                elif obj == bush1:
                    terrain[14][cols+len(obj)//2] = bush1num
                elif obj == bush2:
                    terrain[14][cols+len(obj)//2] = bush2num
                elif obj == bush3:
                    terrain[14][cols+len(obj)//2] = bush3num
        return drawHill(rows,cols-random.randint(2,10),terrain)
        #return drawHill(rows,cols-random.randint(6,10),terrain)

def createTerrain(rows,cols,level):
    terrain = make2dList(rows,cols,0)
    drawFloor(rows,cols,terrain,level)
    drawHoles(rows,cols,terrain,level)
    drawBricks(rows,cols,terrain,level)
    drawClouds(rows,cols,terrain)
    drawTube(rows,cols,terrain,level)
    drawHill(rows,cols,terrain)
    drawMountain(rows,cols,terrain,level)
    if level == 0:
        terrain[7][10] = 100
    return terrain

#############################################
# Global Variables
#############################################

def appStarted(app):
    app.gameMode = "Start"
    #pygame.mixer.init()
    #app.sound = Sound("themesong.mp3")
    app.gamePaused = False
    app.rows,app.cols,app.cellSize,app.margin = gameDimensions()
    app.level = 0
    app.terrain = createTerrain(app.rows,app.cols,app.level)
    app.mapX = 0
    app.marioX = app.margin+2.5*app.cellSize
    app.marioY = app.margin+14.5*app.cellSize
    app.marioVH, app.marioVV = 0,0
    app.marioDied = 0
    app.right = False
    app.timeRef = time.time()
    app.time = 0
    app.timerDelay = 1
    app.speed = 10
    app.mover = 0
    app.moveRight=0
    app.moveLeft = 0
    app.mute = False
    app.blockSet = [0,3,5,6,7,8,9]
    #####################
    ### IMAGES ###
    #####################
    # CITATIONS
    # Mario Sprite Sheet: https://www.pinterest.com/pin/583990276653563224/
    # Super Mario bros sign: https://venturebeat.com/2015/09/13/super-mario-\
    # bros-is-30-years-old-today-and-deserves-our-thanks/
    # Super Mario Sign 1: https://www.youtube.com/watch?v=u32cg6WsfEw
    # Super Mario Sign 2: https://en.wikipedia.org/wiki/Super_Mario
    # Scroll 2: http://clipart-library.com/clipart/scroll-cliparts_4.htm
    # Game over lettering: https://vocal.media/gamers/game-over-1
    # Other images: https://line.17qq.com/articles/hcplhdglv_p2.html  ,
    # created by created by metalichotdog@hotmail.com.
    # gamer font: https://www.dafont.com/search.php?q=gamer
    IMG1 = app.loadImage('floorBlock.png')
    app.floorBlock = app.scaleImage(IMG1,1/30)
    IMG2 = app.loadImage('cloud.png')
    app.cloud = app.scaleImage(IMG2,1/4.8)
    IMG3 = app.loadImage('doubleCloud.png')
    app.doubleCloud = app.scaleImage(IMG3,1/4.8)
    IMG4 = app.loadImage('brickBlock.png')
    app.brick = app.scaleImage(IMG4,1/8)
    IMG5 = app.loadImage('hill1.png')
    app.hill1 = app.scaleImage(IMG5,5/2)
    IMG6 = app.loadImage('hill2.png')
    app.hill2 = app.scaleImage(IMG6,5/2)
    IMG7 = app.loadImage('bush1.png')
    app.bush1 = app.scaleImage(IMG7,5/2)
    IMG8 = app.loadImage('bush2.png')
    app.bush2 = app.scaleImage(IMG8,5/2)
    IMG85 = app.loadImage('bush3.png')
    app.bush3 = app.scaleImage(IMG85,5/2)
    IMG9 = app.loadImage('goomba.png')
    spriteSheetG = app.scaleImage(IMG9,5/2)
    IMG10 = app.loadImage('marioDead.png')
    app.marioDead = app.scaleImage(IMG10,5/2)
    IMG11 = app.loadImage('marioBrosSign.png')
    app.marioSign = app.scaleImage(IMG11,1/4)
    IMG12 = app.loadImage('tubeL.png')
    app.tubeL = app.scaleImage(IMG12,5/2)
    IMG13 = app.loadImage('tubeR.png')
    app.tubeR = app.scaleImage(IMG13,5/2)
    IMG14 = app.loadImage('tubeTopL.png')
    app.tubeTopL = app.scaleImage(IMG14,5/2)
    IMG15 = app.loadImage('tubeTopR.png')
    app.tubeTopR = app.scaleImage(IMG15,5/2)
    app.empty = app.loadImage('None.png')
    IMG16 = app.loadImage('chomper.png')
    spriteSheetC = app.scaleImage(IMG16,5/2)
    IMG17 = app.loadImage('slantBlock.png')
    app.slantBlock = app.scaleImage(IMG17,1/30)
    IMG18 = app.loadImage('slantBlock2.png')
    app.slantBlock2 = app.scaleImage(IMG18,1/30)
    IMG19 = app.loadImage('AI.png')
    app.AI = app.scaleImage(IMG19,5/2)
    IMG20 = app.loadImage('startscreen.png')
    app.marioScreen = app.scaleImage(IMG20,2/3)
    IMG21 = app.loadImage('pressEnter.png')
    app.enter = app.scaleImage(IMG21,1/3)
    app.gameOver = app.loadImage("gameOver.png")
    IMG22 = app.loadImage('starttube.png')
    app.starttube = app.scaleImage(IMG22,1/3)
    IMG23 = app.loadImage('scroll.png')
    app.scroll = app.scaleImage(IMG23,7/10)
    IMG25 = app.loadImage('scroll2.png')
    app.scroll2 = app.scaleImage(IMG25,1/3)
    app.chomperSprites = []
    for i in range(2):
        sprite = spriteSheetC.crop((50*i,0,50+50*i,58))
        app.chomperSprites.append(sprite)
    app.cSpriteCounter = 0
    app.chomper = app.chomperSprites[app.cSpriteCounter]
    app.chomperS = app.scaleImage(app.chomper,2)
    app.chomperY = 2
    app.goombaSprites = []
    app.goombas = []
    for i in range(3):
        sprite = spriteSheetG.crop((50*i,0,50+50*i,40))
        app.goombaSprites.append(sprite)
    IMGM = app.loadImage('mario.png')
    spriteSheet = app.scaleImage(IMGM,5/2)
    app.marioSpritesR = []
    for i in range(6):
        sprite = spriteSheet.crop((75*i,0,75+75*i,40))
        app.marioSpritesR.append(sprite)
    app.marioRunningR = []
    for sprite in range(1,4):
        app.marioRunningR.append(app.marioSpritesR[sprite])
    spriteSheet = IMGM.transpose(Image.FLIP_LEFT_RIGHT)
    spriteSheet = app.scaleImage(spriteSheet,5/2)
    app.marioSpritesL = []
    for i in range (6):
        sprite = spriteSheet.crop((75*i,0,75+75*i,40))
        app.marioSpritesL.append(sprite)
    app.marioRunningL = []
    for sprite in range(1,4):
        app.marioRunningL.append(app.marioSpritesL[sprite])
    app.mSpriteCounter = 0 
    app.mario = app.marioSpritesR[app.mSpriteCounter]
    app.dy = 0
    app.isJumping = False
    app.isFalling = False
    app.g = 1.5
    app.gSpriteCounter = 0
    app.goomba = app.goombaSprites[app.gSpriteCounter]
    IMG = getCachedImage(app,app.goomba)
    firstGoomba = Goomba(cx=800, cy=590, img=IMG, status= 'alive', speed=-3)
    secondGoomba = Goomba(cx=1600, cy=200,img=IMG,status='alive',speed=-3)
    app.goombas.append(firstGoomba)
    app.goombas.append(secondGoomba)
    app.goombaCount = 0
    app.chompers = []
    app.marCol = int((app.marioX-app.mapX)//app.cellSize)
    app.marRow = int(app.marioY//app.cellSize)  
    app.tracker = -app.margin
    app.distance = 0
    app.debug = 0
    app.killGoomba = False
    app.graph = {
        0: [1,10],
        1: [0,2,11],
        2: [1,3,12],
        3: [2,4,13],
        4: [3,14,5],
        5: [4,15],
        10: [0,11,20],
        11: [1,10,12,21],
        12: [2,11,13,22],
        13: [3,12,14,23],
        14: [4,13,24,15],
        15: [5,14,25],
        20: [10,21,30],
        21: [11,20,22,31],
        22: [12,21,23,32],
        23: [13,22,24,33],
        24: [14,23,34,25],
        25: [15,24,35],
        30: [20,31],
        31: [21,30,32],
        32: [22,31,33],
        33: [23,32,34],
        34: [24,33,35],
        35: [34,25]
        }
    app.node = 0
    x,y = getGraphCoords(app.graph,app.node)
    app.AIX = x
    app.AIY = y
    app.AIspeed = 2
    app.AImoving = False
    app.path = getMarioPath(app,app.graph,app.node)

def appStopped(app):
    pygame.mixer.music.stop()

#############################################
# Key Pressed Functions
#############################################

def keyPressed(app,event):
    if event.key=='r':
        appStarted(app)
        pygame.mixer.music.stop()
    if app.gameMode == 'Paused' or app.gameMode == 'Over':
        return
    if event.key=='Enter':
        app.gameMode = 'Play'
        pygame.mixer.music.play(-1)
    if event.key == 'm' or event.key == 'M':
        app.mute = not app.mute
        if app.mute == True:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
    if event.key=='Left':
        app.moveLeft = time.time()
        app.moveRight = 0
        app.speed = -abs(app.speed)
    if event.key=='Right':
        app.moveRight = time.time()
        app.moveLeft = 0
        app.speed = abs(app.speed)
    if event.key=='Space' and not app.isJumping:
        app.dy = -22
        app.isJumping = True
        jumpSound.play()
    if event.key=='i' or event.key=='I':
        if app.gameMode == 'Start':
            app.gameMode = 'Instructions'
    if event.key=='f':
        app.AImoving = False
    if event.key=='a':
        if app.gameMode=="Start":
            app.AImoving = not(app.AImoving)
    if event.key=='p':
        if app.gameMode=='Play':
            app.gamePaused = not app.gamePaused

#############################################
# Timer Fired Functions
#############################################

def timerFired(app):
    app.marCol = int(((app.marioX-app.mapX)//app.cellSize)-app.distance)
    app.marRow = int(app.marioY//app.cellSize)    
    app.time = int((time.time()-app.timeRef))
    if app.gamePaused == True:
        return
    if app.gameMode == 'Play':
        goombaRules(app)
        checkForLevelChange(app)
    if app.killGoomba:
        killGoomba(app)
        app.goombaStomp = True
    if time.time() - app.moveRight<0.3:
        marioMoveRight(app)
    elif time.time()-app.moveLeft<0.3:
        marioMoveLeft(app)
    else:
        if app.moveRight>=app.moveLeft:
            app.mario = app.marioSpritesR[0]
        else:
            app.mario = app.marioSpritesL[5]   
    if app.isJumping:
        marioJumping(app)
    if app.gameMode=='Play':
        if app.terrain[app.marRow+1][app.marCol]==1 and \
            (app.terrain[app.marRow][app.marCol]==0 or\
            app.terrain[app.marRow][app.marCol]==1) and app.marRow<14+1 and\
            app.isJumping==False and app.gameMode=='Play':
            x0,x1,y0,y1 = getCellBounds(app,app.marRow+1,app.marCol)
            app.marioY = y0-20
        if (int((time.time()*10)%10))%2==0:
            app.gSpriteCounter = 0
        else:
            app.gSpriteCounter = 1
    if app.gameMode == 'Play' and app.level>1:
        for chomper in app.chompers:
            IMG = getCachedImage(app,app.chomperSprites[app.cSpriteCounter])
            chomper.img = IMG
            chomper.cy -= chomper.speed
            if chomper.cy == chomper.top:
                chomper.speed = -(chomper.speed)
            elif chomper.cy == chomper.bottom:
                chomper.speed = -(chomper.speed)
            if abs(app.marioX-chomper.cx)<30 and abs(app.marioY-chomper.cy)<40:
                app.mario = app.marioDead
                app.gameMode = 'Dying'
                app.marioX -= 5
        if (int((time.time()*10)%10))%2==0:
            app.cSpriteCounter = 0
        else:
            app.cSpriteCounter = 1
    if app.gameMode == 'Dying':
        if app.marioDied == 0:
            killMario.play()
            pygame.mixer.music.stop()
        app.marioDied +=1
        app.mario = app.marioDead
        app.marioY+=5
    if app.isJumping==False and app.gameMode=='Play':
        if app.terrain[app.marRow+1][app.marCol] in app.blockSet:
            app.isFalling=True
    if app.isFalling and app.gameMode=="Play":
        if app.moveRight>=app.moveLeft:
            app.mario = app.marioSpritesR[5]
        else:
            app.mario = app.marioSpritesL[0]
        app.marioY = app.marioY + app.dy
        app.dy = 15
        app.dy -= app.g
        if app.terrain[app.marRow+1][app.marCol]not in app.blockSet:
            app.isFalling=False
            x0,x1,y0,y1 = getCellBounds(app,app.marRow+1,app.marCol)
            app.marioY = y0-20
    if app.marioY > app.margin+15*app.cellSize:
        app.gameMode = 'Dying' 
        if app.marioY-20>app.height:
            app.gameMode = 'Over'
    if app.debug == app.cellSize:
        app.debug = 0
        app.distance += 1
        for row in range(len(app.terrain)):
            app.terrain[row] = app.terrain[row][1::]
    if app.AImoving == True and app.gameMode == "Play":
        catchMario(app)
    if abs(app.marioX-app.AIX)<35 and abs(app.marioY-app.AIY)<40:
        app.gameMode = 'Dying'
    if app.gameMode == "Over":
        app.chompas = []

#############################################
# Mario Functions / User Experience
#############################################

def moveisLegal(app,move):
    marCol = int(((app.marioX-app.mapX+move)//app.cellSize)-app.distance)
    if app.marioX+move-app.cellSize//2 >= app.margin:
        if app.terrain[app.marRow][marCol] in app.blockSet:
            return True
        elif app.terrain[app.marRow][marCol]==15 and move>0:
            return True
        elif app.terrain[app.marRow][marCol]==14 and move<0:
            return True
    return False

def checkForLevelChange(app):
    x0,x1,y0,y1 = getCellBounds(app,0,len(app.terrain[0]))
    if x1<app.width:
        app.level += 1
        newTerrain = createTerrain(app.rows,app.cols,app.level)
        app.chompers = []
        for row in range(len(app.terrain)):
            app.terrain[row]+=newTerrain[row]
        createGoomba(app,app.level)
        createChomper(app,app.level)

def marioMoveRight(app):
    if app.gameMode != 'Play':
        return
    if (int((time.time()*10)%10))%2 == 0:
        app.mSpriteCounter=(1+app.mSpriteCounter)%len(app.marioRunningR)
    app.mario = app.marioRunningR[app.mSpriteCounter]
    if moveisLegal(app,app.speed):
        if app.terrain[app.marRow+1][app.marCol]==15 or \
            app.terrain[app.marRow][app.marCol]==15:
                app.marioY += app.speed
        if app.width//2 < app.marioX + app.speed:
            app.mapX -= app.speed
            app.debug += app.speed
            for goomba in app.goombas:
                goomba.cx -= app.speed
            for chomper in app.chompers:
                chomper.cx -= app.speed
        else:
            app.marioX += app.speed
    elif app.terrain[app.marRow][app.marCol+1]==14 or \
        app.terrain[app.marRow][app.marCol]==14:
        if app.width//2 < app.marioX + app.speed:
            app.mapX -= app.speed
            app.debug += app.speed
            app.marioY-=app.speed
            for goomba in app.goombas:
                goomba.cx -= app.speed
            for chomper in app.chompers:
                chomper.cx -= app.speed
        else:
            app.marioX+=app.speed
            app.marioY-=app.speed

def marioMoveLeft(app):
    app.mario = app.marioRunningL[app.mSpriteCounter]
    if (int((time.time()*10)%10))%2 == 0:
        app.mSpriteCounter=(1+app.mSpriteCounter)%len(app.marioRunningL)
    if moveisLegal(app,app.speed):
        if app.terrain[app.marRow+1][app.marCol]==14 or \
            app.terrain[app.marRow][app.marCol]==14:
                app.marioY -= app.speed
        app.marioX+=app.speed
    elif app.terrain[app.marRow][app.marCol-1]==15 or \
        app.terrain[app.marRow][app.marCol]==15:
        app.marioX += app.speed
        app.marioY += app.speed

def marioJumping(app):
    if app.moveRight>=app.moveLeft:
        app.mario = app.marioSpritesR[5]
    else:
        app.mario = app.marioSpritesL[0]
    if app.terrain[app.marRow-1][app.marCol]not in app.blockSet and\
        app.gameMode=='Play':
        if app.dy<0 and app.terrain[app.marRow-1][app.marCol]==2:
            app.terrain[app.marRow-1][app.marCol] = 0
        app.isJumping = False
        app.isFalling = True
        x0,x1,y0,y1 = getCellBounds(app,app.marRow-1,app.marCol)
        app.marioY = y1+20
    if app.terrain[app.marRow+1][app.marCol]not in app.blockSet and \
        app.dy>0:
        app.isJumping = False
        app.dy = 0
        x0,x1,y0,y1 = getCellBounds(app,app.marRow+1,app.marCol)
        if app.terrain[app.marRow+1][app.marCol]!=14 and \
            app.terrain[app.marRow+1][app.marCol]!=15:
            app.marioY = y0-20
        elif app.terrain[app.marRow+1][app.marCol]==15:
            app.marioY = y1-20-40+(app.marioX-8)%40
        else: 
            app.marioY = y1-20-(app.marioX-8)%40
    elif app.terrain[app.marRow+1][app.marCol]in app.blockSet and \
        app.marRow+1==15:
        app.gameMode = 'Dying'
        app.isJumping = False
        app.isFalling = True
        app.marioY += 20
    app.marioY = min(app.marioY + app.dy, app.margin+14.5*app.cellSize)
    app.dy += app.g
#############################################
# Enemy Functions
#############################################

Goomba = make_dataclass("Goomba", ['cx','cy','img','status','speed'])
Chomper = make_dataclass("Chomper",['cx','cy','img','speed','top','bottom'])

#### Goombas ####

def changeGoombaDir(app,goomba,move,gRow):
    gCol = int(((goomba.cx-app.mapX)//app.cellSize)-app.distance)
    if app.terrain[gRow][gCol]not in app.blockSet and \
        app.terrain[gRow][gCol]!=14 and app.terrain[gRow][gCol]!=15:
        return True
    return False

def createGoomba(app,level):
    IMG = getCachedImage(app,app.goomba)
    for i in range(level+5):
        randY = random.choice([260,420])
        randX = random.choice([1600,2000,2480])
        randD = random.choice([140,40,220])
        col = int(((1200-app.mapX)//app.cellSize)-app.distance)
        row = int(588//app.cellSize)
        if app.terrain[row][col]in app.blockSet and \
            app.terrain[row+1][col]in app.blockSet and\
            app.terrain[row-1][col]in app.blockSet:
            if 1200+randD*i<2000:  
                newGoomba = Goomba(cx=1200+randD*i, cy=588, img=IMG, 
                status= 'alive', speed=-3)
            else:
                newGoomba = Goomba(cx=1000+randD*i,cy=588,img=IMG,
                status='alive',speed=-3)
        else:
            if app.time%2==0 and i<=3:
                newGoomba = Goomba(cx=1056+60*i, cy=588, img=IMG, 
            status= 'alive', speed=-3)
            else:
                newGoomba = Goomba(cx=randX+randD*i, cy=randY, img=IMG, 
            status= 'alive', speed=-3)
        app.goombas.append(newGoomba)

def goombaRules(app):
    if (int((time.time()*10)%10))%2==0:
        app.gSpriteCounter = 0
    else:
        app.gSpriteCounter = 1
    IMG = getCachedImage(app,app.goombaSprites[app.gSpriteCounter])
    for goomba in app.goombas:
        gCol = int(((goomba.cx-app.mapX)//app.cellSize)-app.distance)
        gRow = int(goomba.cy//app.cellSize)
        if goomba.cx<(5/4)*app.width and goomba.cy<app.height:
            if gRow >= 15:
                goomba.cy+=8
                goomba.cx-=goomba.speed
            elif gCol<len(app.terrain[0]) and gRow<len(app.terrain):
                if app.terrain[gRow+1][gCol] in app.blockSet:
                    goomba.cy+=10
                    goomba.cx-=goomba.speed
                else:
                    if goomba.cy == 596:
                        goomba.cy = 590
                    if app.terrain[gRow][gCol] in app.blockSet and \
                        app.terrain[gRow+1][gCol] not in app.blockSet\
                        and app.terrain[gRow+1][gCol]!=14 and\
                        app.terrain[gRow+1][gCol]!=15:
                        x0,x1,y0,y1 = getCellBounds(app,gRow+1,gCol)
                        goomba.cy = y0-20
                if changeGoombaDir(app,goomba,goomba.speed,gRow):
                    goomba.speed = -goomba.speed
                if goomba.speed < 0:
                    if app.terrain[gRow][gCol] in [12,13,11,10,1]:
                            goomba.cx-=5
                    if (app.terrain[gRow][gCol]==14 or \
                    app.terrain[gRow+1][gCol]==14):
                        goomba.cy-=goomba.speed
                    if app.terrain[gRow][gCol]==15:
                        goomba.cy+=goomba.speed
                if goomba.speed > 0:
                    if app.terrain[gRow][gCol]==14:
                        goomba.cy-=goomba.speed
                    if app.terrain[gRow][gCol]==15 or\
                        app.terrain[gRow+1][gCol]==15:
                        goomba.cy+=goomba.speed
        if goomba.cy>=app.height-app.margin or goomba.cx<0:
            index = (app.goombas.index(goomba))
            app.goombas.pop(index)
        goomba.cx+=goomba.speed
        goomba.img = IMG
        if abs(app.marioX-goomba.cx)<20 and abs(app.marioY-goomba.cy)<40\
            and (app.isFalling or app.isJumping) and app.goomba!= app.empty:
            app.killGoomba = True
            app.killGoombaTime = time.time()
            goomba.status = 'dead'
        elif abs(app.marioX-goomba.cx)<20 and abs(app.marioY-goomba.cy)<20\
            and app.killGoomba == False and goomba.status == 'alive':
            app.mario = app.marioDead
            app.gameMode = 'Dying'
            app.marioX -= 5

def killGoomba(app):
    IMG = getCachedImage(app,app.goombaSprites[2])
    if time.time()-app.killGoombaTime<0.35:
        if app.goombaCount==0:
            stompGoomba.play()
        app.goombaCount += 1
        app.marioY-=35
        for goomba in app.goombas:
            if goomba.status == 'dead':
                goomba.img = IMG
    else:
        app.isFalling = True
        app.killGoomba = False
        app.goombaCount = 0
        for goomba in app.goombas:
            if goomba.status == 'dead':
                index = (app.goombas.index(goomba))
                app.goombas.pop(index)

#### Chompers ####

def createChomper(app,level):
    IMG = getCachedImage(app,app.chomper)
    for row in range(len(app.terrain)):
        for col in range(len(app.terrain[0])):
            chompaExists = random.choice([0,1,1])
            if chompaExists == 0:
                continue
            if app.level<4:
                y = random.choice([40,50,60])
            else:
                y = random.choice([10,20,30,40])
            if app.terrain[row][col] == 12:
                x0,x1,y0,y1 = getCellBounds(app,row,col)
                newChomper = Chomper(cx=x1,cy=y1+y,img=IMG,speed=app.chomperY,
                top=y0-28,bottom=y1+y)
                app.chompers.append(newChomper)

#############################################
# AI 
#############################################

def moveAI(app,start,end):
    if start == end:
        return
    if start//10 == end//10:
        if start<end:
            app.AIX += app.AIspeed
        else:
            app.AIX -= app.AIspeed
    if start%10 == end%10:
        if start<end:
            app.AIY += app.AIspeed
        else:
            app.AIY -= app.AIspeed

def getMarioPath(app,graph,currNode):
    endNode = getMarioNode(graph,app.marioX,app.marioY)
    path = bfs(currNode,endNode,[(currNode, [currNode],)],graph)
    return path

def distance(x0,y0,x1,y1):
    return ((x0-x1)**2+(y0-y1)**2)**0.5

def getGraphCoords(graph,node):
    x = 100*((node%10)+1)
    y = 160*((node//10)+1) - 50
    if node == 0:
        pass
    return (x,y)

def getMarioNode(graph,mX,mY):
    bestDistance = None
    bestNode = None
    for parent in graph:
        for node in graph[parent]:
            x,y = getGraphCoords(graph,node)
            length = distance(x,y,mX,mY)
            if bestDistance == None or length<bestDistance:
                bestDistance = length
                bestNode = node
    return bestNode

def bfs(start, end, queue, graph):
    newQueue = copy.copy(queue)
    while True:
        if newQueue == []:
            return [start]
        if start == end:
            return [end]
        node, path = newQueue.pop(0)
        lst = (graph[node])
        for val in path:
            if val in lst:
                lst.remove(val)
        for neighbour in lst:
            if end == neighbour:
                result = path + [neighbour]
                return result
            else:
                newQueue.append((neighbour, path+[neighbour]))

def catchMario(app):
    if len(app.path)==1:
        x,y = getGraphCoords(app.graph,app.path[0])
        app.node = app.path[0]
        app.AIX = x
        app.AIY = y
        app.path = getMarioPath(app,app.graph,app.node)
    else:
        x,y = getGraphCoords(app.graph,app.path[1])
        if app.AIX==x and app.AIY==y:
            app.node = app.path[1]
            app.AIX = x
            app.AIY = y
            app.path = getMarioPath(app,app.graph,app.node)
        else:
            moveAI(app,app.path[0],app.path[1])

#############################################
# Draw / View Functions
#############################################

#### Characters ####

def drawMario(app,canvas):
    IMG = getCachedImage(app,app.mario)
    canvas.create_image(app.marioX,app.marioY,
    image=IMG)

def drawGoomba(app,canvas):
    for goomba in app.goombas:
        canvas.create_image(goomba.cx,goomba.cy,image=goomba.img)
    drawMargin(app,canvas)

def drawAI(app,canvas):
    if (app.gameMode == "Play" or app.gameMode == 'Dying') and \
        app.AImoving==True:
        IMG = getCachedImage(app,app.AI)
        canvas.create_image(app.AIX,app.AIY,image=IMG)

def drawChomper(app,canvas):
    if app.gameMode=="Play" or "Dying":
        for chomper in app.chompers:
            canvas.create_image(chomper.cx,chomper.cy,image=chomper.img)

#### Game Background ####

def drawBackground(app,canvas):
    if app.gameMode == "Start" or app.gameMode=="Instructions":
        color = 'light green'
    elif app.gameMode == "Play" or "Dying":
        color = 'skyblue'
        canvas.create_text(app.width//2,50,text=f'Distance: {app.distance}', 
        font='Arial 20 bold')
    if app.gameMode == "Over":
        color = 'maroon'
    canvas.create_rectangle(app.margin,app.margin,app.width-app.margin,
    app.height-app.margin,fill=color,width=0)

def drawMargin(app,canvas):
    canvas.create_rectangle(0,0,app.margin,app.height,fill='white',width=0)
    canvas.create_rectangle(app.width-app.margin,0,app.width,app.height,
    fill='white',width=0)
    canvas.create_rectangle(0,app.height-app.margin,app.width,app.height,
    fill='white',width=0)

def drawScore(app,canvas):
    if app.gameMode in ['Play','Dying','Paused']:
        canvas.create_text(app.width//2,50,text=f'SCORE: {app.distance}',
        font = "Arial 20 bold",fill='White')

#### Terrain Board ####

def getCellBounds(app,row,col):
    x0 = app.margin+app.cellSize*col+app.mapX+app.distance*app.cellSize
    x1 = x0+app.cellSize
    y0 = app.cellSize*row+app.margin
    y1 = y0+app.cellSize
    return x0,x1,y0,y1

def drawCell(app,canvas,row,col,IMG):
    x = app.margin+app.cellSize*col+app.mapX+app.cellSize/2
    if IMG==app.cloud:
        if app.terrain[row][col-1] == 3:
            IMG = getCachedImage(app,app.doubleCloud)
            canvas.create_image(x+app.distance*app.cellSize,
        app.cellSize*row+app.margin+app.cellSize/2,image=IMG)
        elif app.terrain[row][col-1]!=3 and app.terrain[row][col+1]!=3:
            IMG = getCachedImage(app,IMG)
            canvas.create_image(x+app.distance*app.cellSize,
        app.cellSize*row+app.margin+app.cellSize/2,image=IMG)
    else:
        IMG = getCachedImage(app,IMG)
        canvas.create_image(x+app.distance*app.cellSize,
    app.cellSize*row+app.margin+app.cellSize/2,image=IMG)

def drawBoard(app,canvas):
    for row in range(len(app.terrain)):
        for col in range(len(app.terrain[0])):
            if app.terrain[row][col]==1:
                drawCell(app,canvas,row,col,app.floorBlock)
            elif app.terrain[row][col]==2:
                drawCell(app,canvas,row,col,app.brick)
            elif app.terrain[row][col]==3:
                drawCell(app,canvas,row,col,app.cloud)
            elif app.terrain[row][col]==5:
                drawCell(app,canvas,row,col,app.hill1)
            elif app.terrain[row][col]==6:
                drawCell(app,canvas,row-20,col,app.hill2)
            elif app.terrain[row][col]==7:
                drawCell(app,canvas,row,col,app.bush1)
            elif app.terrain[row][col]==8:
                drawCell(app,canvas,row,col,app.bush2)
            elif app.terrain[row][col]==9:
                drawCell(app,canvas,row,col,app.bush3)
            elif app.terrain[row][col]==10:
                drawCell(app,canvas,row,col,app.tubeL)
            elif app.terrain[row][col]==11:
                drawCell(app,canvas,row,col,app.tubeR)
            elif app.terrain[row][col]==12:
                drawCell(app,canvas,row,col,app.tubeTopL)
            elif app.terrain[row][col]==13:
                drawCell(app,canvas,row,col,app.tubeTopR)
            elif app.terrain[row][col]==14:
                drawCell(app,canvas,row,col,app.slantBlock)
            elif app.terrain[row][col]==15:
                drawCell(app,canvas,row,col,app.slantBlock2)
            elif app.terrain[row][col]==100:
                drawCell(app,canvas,row,col-4,app.marioSign)

#### Home and Game Over Screens ####

def homeScreen(app,canvas):
    if app.gameMode == 'Start':
        IMG = getCachedImage(app,app.marioScreen)
        IMG2 = getCachedImage(app,app.enter)
        IMG5 = getCachedImage(app,app.scroll2)
        canvas.create_image(app.width//2,app.height//4+80,image=IMG)
        canvas.create_rectangle(app.width//2-150,420,app.width//2+150,520,
        fill='pink',width=0)
        canvas.create_image(app.width//2,app.height//2+100,
        image=IMG2)
        canvas.create_image(app.width-330,610,image=IMG5)
        canvas.create_text(app.width-330,690,
        text="Press 'I' to read instructions!",font='Arial 20 italic')
    if app.gameMode == 'Instructions'or app.gameMode=='Start':  
        IMG3 = getCachedImage(app,app.starttube)
        IMG4 = getCachedImage(app,app.chomperS)
        canvas.create_image(app.width//8,611,image=IMG3)
        canvas.create_image(app.width//(8/7),611,image=IMG3)
        canvas.create_image(app.width//8,437,image=IMG4)
        canvas.create_image(app.width//(8/7),437,image=IMG4)
    if app.AImoving==False and app.gameMode=='Start':
        canvas.create_oval(330-60,610-60,330+60,610+60,
        fill='Red',width=4)
        canvas.create_text(330,630,text="OFF",font="Arial 30 bold")
        canvas.create_text(330,690,text="Press 'A' to turn AI mode on!",
        font='Arial 20 italic')
        canvas.create_text(330,595,text="AI MODE",font='Arial 24 bold')
    elif app.AImoving==True and app.gameMode=='Start':
        canvas.create_oval(330-60,610-60,330+60,610+60,
        fill='Green',width=4)
        canvas.create_text(330,630,text="ON",font="Arial 30 bold")
        canvas.create_text(330,690,text="Press 'A' to turn AI mode off!",
        font='Arial 20 italic')
        canvas.create_text(330,595,text="AI MODE",font='Arial 24 bold')

def instructions(app,canvas):
    if app.gameMode == 'Instructions':
        IMG = getCachedImage(app,app.scroll)
        canvas.create_image(app.width//2,app.height//2,image=IMG)
        canvas.create_text(app.width//2,app.height//8+70,text= "INSTRUCTIONS",
        font='Verdana 32 bold')
        canvas.create_text(app.width//2,245,
        text='Use the left and right arrow keys to move',
        font='Verdana 19')
        canvas.create_text(app.width//2,295,
        text='Use the space bar to jump',
        font= 'Verdana 20')
        canvas.create_text(app.width//2,460,
        text='Avoid getting hit by the Goombas,\n Chompas, and AI!!',
        font= 'Verdana 20')
        canvas.create_text(app.width//2+10,405,
        text='Jump on the goombas to kill them!',font= 'Verdana 20')
        canvas.create_text(app.width//2,520,
        text='Get the highest score by going',font= 'Verdana 20')
        canvas.create_text(app.width//2,560,
        text='the longest distance without being killed!',font= 'Verdana 20')
        canvas.create_text(app.width//2,620,
        text='Press Enter to start!',font='Verdana 18 italic')
        canvas.create_text(app.width//2,350,
        text='Press P to pause and M to mute',font='Verdana 20')


def drawPaused(app,canvas):
    if app.gamePaused==True:
        canvas.create_rectangle(app.width//2-40,app.height//2-70,
        app.width//2-10,
        app.height//2+60,fill='White',width=0)
        canvas.create_rectangle(app.width//2+10,app.height//2-70,
        app.width//2+40,
        app.height//2+60,fill='White',width=0)
        canvas.create_text(app.width//2,app.height//2+90,
        text="GAME PAUSED",font='Verdana 33 bold',fill='White')

def drawGameOver(app,canvas):
    if app.gameMode == "Over":
        canvas.create_rectangle(app.margin,app.margin,app.width-app.margin,
        app.height-app.margin,fill='Maroon',width=0)
        IMG = getCachedImage(app,app.gameOver)
        canvas.create_rectangle(50,app.height//2-60,app.width-50,
        app.height//2+80,fill='blue',width=0)
        canvas.create_image(app.width//2,app.height//2,
        image=IMG,)
        canvas.create_text(app.width//2,app.height//2+120,
        text=f'SCORE: {app.distance}',font = 'Arial 40',fill='white')
        canvas.create_text(app.width//2,app.height//2+175,
        text='Press R to restart!',font='Arial 25',fill='white')
        for chomper in app.chompers:
            canvas.create_image(chomper.cx,chomper.cy,image=chomper.img)

def drawGame(app,canvas):
    if app.gameMode == 'Play' or app.gameMode=='Dying':
        drawChomper(app,canvas)
        drawBoard(app,canvas)
        drawGoomba(app,canvas)
        drawMario(app,canvas)

# Used to test the AI algorithm, not shown in the game
def drawGraph(graph,canvas):
    for parent in graph:
        for node in graph[parent]:
            x,y = getGraphCoords(graph,node)
            canvas.create_oval(x-10,y-10,x+10,y+10,
            fill='pink')

def redrawAll(app,canvas):
    drawBackground(app,canvas)
    drawScore(app,canvas)
    homeScreen(app,canvas)
    instructions(app,canvas)
    drawGame(app,canvas)
    drawGameOver(app,canvas)
    drawAI(app,canvas)
    drawPaused(app,canvas)

def main():
    playMario()

if (__name__ == '__main__'):
    main()

