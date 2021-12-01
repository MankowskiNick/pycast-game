
import pygame, sys
from pygame.locals import *
from genericpath import exists

def createEmptyMap(mWidth, mHeight):
    #Define map size
    mWidth = int(input("Input width: "))
    mHeight = int(input("Input map height: "))

    #Declare empty map variable
    currentMap = []

    #Fill map with empty space
    for y in range(0,mHeight,1):
        temp = []
        for x in range(0,mWidth,1):
            temp.append(0)
        currentMap.append(temp)
    
    return currentMap, mWidth, mHeight

def getMapCoords(mCoords, blockSize):
    mx, my = mCoords
    mapX = int(mx / blockSize)
    mapY = int(my / blockSize)
    return mapX, mapY

#playerX, playerY, playerAngle, level as inputs
def renderMap(drawMap, screen, blockSize, white, spriteList):
	for x in range(0,len(drawMap[0])):
		for y in range(0,len(drawMap)):
			if (drawMap[y][x] > 0):screen.blit(pygame.transform.scale(spriteList[drawMap[y][x]], (blockSize, blockSize)), (x * blockSize, y * blockSize))
			else:pygame.draw.rect(screen, white, pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize), 2)

def getBlocksize(mWidth, mHeight, width, height):
    if (width / mWidth > height / mHeight):
        bSize = height / mHeight
    else:
        bSize = width / mWidth
    return bSize

def getMapDimensions(drawMap):
    return len(drawMap[0]), len(drawMap)

def saveMap(drawMap):
    fileName = input("Enter the name of the file to save to(without file extension): ")
    if (exists("levels/" + fileName + ".leveldata")):
        file = open("levels/" + fileName + ".leveldata", "w")
    else:
        file = open("levels/" + fileName + ".leveldata", "x")
    
    #Write map height data to first line of file
    if (len(drawMap[0]) > 9 and len(drawMap) > 9):
        file.write(str(len(drawMap[0])) + " " + str(len(drawMap)) + "\n")
    elif (len(drawMap[0] <= 9)):
        file.write("0" + str(len(drawMap[0])) + " " + str(len(drawMap)) + "\n")
    elif (len(drawMap) <= 9):
        file.write(str(len(drawMap[0])) + " 0" + str(len(drawMap)) + "\n")

    for y in range(0,len(drawMap)):
        temp = ""
        for x in range(0,len(drawMap[y])):
            temp += (str(drawMap[y][x]) + " ")
        temp += "\n"
        file.write(temp)
    file.close()

def loadMapFromFile(fileName):
    if (exists("levels/" + fileName + ".leveldata")):
        loadMap = []
        file = open("levels/" + fileName + ".leveldata")
        fileLines = []
        fileLines = file.readlines()
        currentParser = 0
        mWidth = int(fileLines[0][0:2])
        mHeight = int(fileLines[0][3:5])

        for y in range(1,mHeight + 1):
            temp = []
            currentParser = 0
            for x in range(0,mWidth):
                oldParser = currentParser
                currentParser = fileLines[y].find(" ", oldParser + 1, len(fileLines[y]))
                temp.append(int(fileLines[y][oldParser:currentParser]))
            loadMap.append(temp)
        file.close()
        return loadMap, True, mWidth, mHeight
    else:
        print("File not found.")
        return [], False, 0, 0

def exportMapsToPython():
    exportCount = int(input("How many maps would you like to patch in to the game?: "))
    maps = []

    if exists("LevelData.py"):
        file = open("LevelData.py", "w")
        file.write("")
        del file
        file = open("LevelData.py", "a")
    else:
        file = open("LevelData.py", "x")
    for i in range(0,exportCount):
        tempMap, temp1, temp2, temp3 = loadMapFromFile(input("Enter file name for map #" + str(i+1) + ": "))
        del temp1, temp2, temp3
        file.write("Map" + str(i) + " = [")
        for y in range(0,len(tempMap)):
            file.write("\n    [")
            for x in range(0,len(tempMap[0])):
                file.write(str(tempMap[y][x]))
                if (x == len(tempMap[0]) - 1):
                    file.write("]")
                    if (y != len(tempMap) - 1):
                        file.write(",\n")
                    else:
                        file.write("\n")
                else:
                    file.write(", ")
        file.write("]\n\n")
            
def Main():
    pygame.init()

    frameCount = 0
    size = width, height = (800,600)

    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Map Generator")

    #Define colors
    black = (0,0,0)
    white = (255,255,255)
    gray = (100,100,100)
    red = (255,0,0)
    blue = (0,0,255)

    mapWidth, mapHeight = 0,0
    blockSize = 1

    currentBlockID = 1

    #Define wall textures
    spriteList = {
        1 : pygame.image.load("assets/wall.png"),
        2 : pygame.image.load("assets/window.png"),
        3 : pygame.image.load("assets/trunk.png"),

        1000 : pygame.image.load("assets/barrel.png"),

        2000 : pygame.image.load("assets/enemy.png")
    }

    currentMap, mapWidth, mapHeight = createEmptyMap(mapWidth, mapHeight)

    blockSize = getBlocksize(mapWidth, mapHeight, width, height)

    while True:
        screen.fill(black)
        frameCount+=1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_n:
                    currentBlockID = int(input("Input new block ID:"))
                if event.key == K_s:
                    saveMap(currentMap)
                if event.key == K_o:
                    tempMap, fileExists, mapWidth, mapHeight = loadMapFromFile(input("Enter file name to load(with extension): "))
                    if (fileExists):
                        currentMap = tempMap
                        blockSize = getBlocksize(mapWidth, mapHeight, width, height)
                    else:
                        mapWidth, mapHeight = getMapDimensions(currentMap)
                if event.key == K_e:
                    exportMapsToPython()
            mouseAction = pygame.mouse.get_pressed()
            if (mouseAction[0]):
                mapX, mapY = getMapCoords(pygame.mouse.get_pos(), blockSize)
                if (mapX < len(currentMap[0]) and mapX >= 0 and mapY < len(currentMap) and mapY >= 0):
                    currentMap[mapY][mapX] = currentBlockID
            if (mouseAction[2]):
                mapX, mapY = getMapCoords(pygame.mouse.get_pos())
                if (mapX < len(currentMap[0]) and mapX >= 0 and mapY < len(currentMap) and mapY >= 0):
                    currentMap[mapY][mapX] = 0

        renderMap(currentMap, screen, blockSize, white, spriteList)
        
        pygame.display.flip()
        pygame.display.update()