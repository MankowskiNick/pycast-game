
import pygame, sys, math
import Sprites, NPC
from pygame.locals import *
from Sprites import *
from genericpath import exists

def createEmptyMap(mWidth, mHeight):
    #Define map size
    mWidth = 50
    mHeight = 50

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

def drawOverlay(px, py, screen, blockSize, npcList, drawMap, mapSpriteList):
    for x in range(0,len(drawMap[0])):
        for y in range(0,len(drawMap)):
            if (drawMap[y][x] > 0 and drawMap[y][x] <= 999):screen.blit(mapSpriteList[drawMap[y][x]], (x * blockSize, y * blockSize))
            else:pygame.draw.rect(screen, (255,255,255), pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize), 2)
    for i in range(0,len(npcList)):
        if npcList[i].type > 999:
            screen.blit(mapSpriteList[npcList[i].type], ((npcList[i].x - 0.5) * blockSize, (npcList[i].y - 0.5) * blockSize))
    pygame.draw.circle(screen, (0,0,255),(px * blockSize, py * blockSize), 3)

def getBlocksize(mWidth, mHeight, width, height):
    if (width / mWidth > height / mHeight):
        bSize = height / mHeight
    else:
        bSize = width / mWidth
    return bSize

def getMapDimensions(drawMap):
    return len(drawMap[0]), len(drawMap)

def saveMap(drawMap, fileName, npcList, px, py):
    if (exists("levels/" + fileName + ".leveldata")):
        file = open("levels/" + fileName + ".leveldata", "w")
    else:
        file = open("levels/" + fileName + ".leveldata", "x")

    tempMap = drawMap

    #Add objects to tempMap
    for i in range(len(npcList)):
        tempMap[npcList[i].startY][npcList[i].startX] = npcList[i].type
    
    #Add player position to tempMap
    tempMap[int(px)][int(py)] = -1

    #Write map height data to first line of file
    if (len(tempMap[0]) > 9 and len(tempMap) > 9):
        file.write(str(len(tempMap[0])) + " " + str(len(tempMap)) + "\n")
    elif (len(tempMap[0] <= 9)):
        file.write("0" + str(len(tempMap[0])) + " " + str(len(tempMap)) + "\n")
    elif (len(tempMap) <= 9):
        file.write(str(len(tempMap[0])) + " 0" + str(len(tempMap)) + "\n")

    #Write tempMap to file
    for y in range(0,len(tempMap)):
        temp = ""
        for x in range(0,len(tempMap[y])):
            temp += (str(tempMap[y][x]) + " ")
        temp += "\n"
        file.write(temp)
    file.close()

def loadMapFromFile(fileName):
    if (exists(fileName)):
        loadMap = []
        file = open(fileName)
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

        npcList = NPC.findNPC(loadMap)

        return loadMap, npcList, True, mWidth, mHeight
    else:
        print("File not found.")
        return [], [], False, 0, 0

def exportMapsToPython(fileName, npcList):

    if not exists("levels/" + fileName + ".leveldata"):
        print("Target file not found.")
        return
    if exists("LevelData.py"):
        file = open("LevelData.py", "w")
        file.write("")
        del file
        file = open("LevelData.py", "a")
    else:
        file = open("LevelData.py", "x")
    tempMap, temp1, temp2, temp3, temp4 = loadMapFromFile("levels/" + fileName + ".leveldata")
    del temp1, temp2, temp3, temp4

    for i in range(0,len(npcList)):
        tempMap[npcList[i].startY][npcList[i].startX] = npcList[i].type

    file.write("Map = [")
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
    
    file.write("]\n\ndef load():return Map")

def Main(px, py, currentMap, npcList):
    pygame.init()

    frameCount = 0
    size = width, height = (800,600)

    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Map Generator")


    font = pygame.font.Font(None, 30)

    clock = pygame.time.Clock()

    #Define colors
    black = (0,0,0)
    white = (255,255,255)
    gray = (100,100,100)
    red = (255,0,0)
    blue = (0,0,255)

    mapWidth, mapHeight = len(currentMap[0]), len(currentMap)
    #blockSize = 1

    currentBlockID = 1

    mapSpriteList = createSpriteList()

    spriteLookUpTable = list(mapSpriteList.keys())

    blockSize = getBlocksize(mapWidth, mapHeight, width, height)

    currentlyTyping = False
    fileName = ""
    actionType = ""

    textboxWidth, textboxHeight = 500,200

    while True:

        screen.fill(black)
        frameCount+=1

        clock.tick(60)

        pygame.key.set_repeat()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if currentlyTyping:
                    if event.key == K_BACKSPACE:
                        fileName = fileName[:-1]
                    elif event.key == K_RETURN:
                        if actionType == "Save file: ":
                            saveMap(currentMap, fileName, npcList, px, py)
                        if actionType == "Open file: ":
                            tempMap, tempNPCList, fileExists, mapWidth, mapHeight = loadMapFromFile("levels/" + fileName + ".leveldata")
                            if (fileExists):
                                currentMap = tempMap
                                npcList = tempNPCList
                                
                                blockSize = getBlocksize(mapWidth, mapHeight, width, height)
                                for i in range(0,len(spriteLookUpTable)):
                                    mapSpriteList[spriteLookUpTable[i]] = pygame.transform.scale(mapSpriteList[spriteLookUpTable[i]], (blockSize, blockSize))
                                
                            else:
                                mapWidth, mapHeight = getMapDimensions(currentMap)
                        if actionType == "Export file: ":
                            print(fileName)
                            exportMapsToPython(fileName, npcList)
                        currentlyTyping = False
                        fileName = ""
                    else:
                         fileName += event.unicode
                elif event.key == K_q:
                    return currentMap, npcList
                elif event.key == K_s:
                    currentlyTyping = True
                    actionType = "Save file: "
                elif event.key == K_o:
                    currentlyTyping = True
                    actionType = "Open file: "
                elif event.key == K_e:
                    currentlyTyping = True
                    actionType = "Export file: "
                for i in range(0,9):
                    if event.key == i + 49:
                        if (i < len(spriteLookUpTable)):
                            currentBlockID = spriteLookUpTable[i]
            mouseAction = pygame.mouse.get_pressed()
            if (mouseAction[0]):
                mapX, mapY = getMapCoords(pygame.mouse.get_pos(), blockSize)
                canPlace = True
                for i in range(0,len(npcList)):
                    if (mapX == int(npcList[i].x) and mapY == int(npcList[i].y)):
                        canPlace = False
                if canPlace:
                    if (mapX < len(currentMap[0]) and mapX >= 0 and mapY < len(currentMap) and mapY >= 0 and currentBlockID < 1000):
                        currentMap[mapY][mapX] = currentBlockID
                    elif (mapX < len(currentMap[0]) and mapX >= 0 and mapY < len(currentMap) and mapY >= 0 and currentBlockID > 999 and currentBlockID < 2000):
                        npcList.append(NPC.NPC((mapX, mapY), currentBlockID, len(npcList)))
                        currentMap[mapY][mapX] = currentBlockID
                    elif (mapX < len(currentMap[0]) and mapX >= 0 and mapY < len(currentMap) and mapY >= 0 and currentBlockID > 1999):
                        npcList.append(NPC.NPC((mapX, mapY), currentBlockID, len(npcList)))
            if (mouseAction[2]):
                mapX, mapY = getMapCoords(pygame.mouse.get_pos(), blockSize)
                if (mapX < len(currentMap[0]) and mapX >= 0 and mapY < len(currentMap) and mapY >= 0):
                    if currentMap[mapY][mapX] > 999:
                        for i in range(0,len(npcList)):
                            if (mapX == int(npcList[i].x) and mapY == int(npcList[i].y)):
                
                                npcList.remove(npcList[i])

                                for n in range(0,len(npcList)):
                                    npcList[n].updateLabel(n)
                                break
                    currentMap[mapY][mapX] = 0
        
        yCheck = int((height)  / (mapSpriteList[spriteLookUpTable[0]].get_height()*2)) * mapSpriteList[spriteLookUpTable[0]].get_height() * 2
        for i in range(0,len(spriteLookUpTable)):
            xDisplacement = 0
            yDisplacement = i * mapSpriteList[spriteLookUpTable[0]].get_height() * 2
            while yDisplacement >= yCheck:
                xDisplacement += mapSpriteList[spriteLookUpTable[0]].get_width() * 2
                yDisplacement -= yCheck
            screen.blit(pygame.transform.scale(mapSpriteList[spriteLookUpTable[i]], (mapSpriteList[spriteLookUpTable[0]].get_width() * 2, mapSpriteList[spriteLookUpTable[0]].get_height() * 2)), (xDisplacement + height, yDisplacement))
            if (spriteLookUpTable[i] == currentBlockID):
                pygame.draw.rect(screen, (0,255,0), (xDisplacement + height, yDisplacement, mapSpriteList[spriteLookUpTable[i]].get_width()*2, 2))
                pygame.draw.rect(screen, (0,255,0), (xDisplacement + height, yDisplacement, 2, mapSpriteList[spriteLookUpTable[i]].get_height()*2))
                pygame.draw.rect(screen, (0,255,0), (xDisplacement + height + mapSpriteList[spriteLookUpTable[i]].get_width()*2 - 2, yDisplacement, 2, mapSpriteList[spriteLookUpTable[i]].get_height()*2))
                pygame.draw.rect(screen, (0,255,0), (xDisplacement + height, yDisplacement + mapSpriteList[spriteLookUpTable[i]].get_width()*2 - 2, mapSpriteList[spriteLookUpTable[i]].get_width()*2, 2))

        drawOverlay(px, py, screen, blockSize, npcList, currentMap, mapSpriteList)

        if currentlyTyping:
            pygame.draw.rect(screen, (255,255,255), ((width / 2) - (textboxWidth / 2), (height / 2) - (textboxHeight / 2), textboxWidth, textboxHeight))
            pygame.draw.rect(screen, (128,128,128), ((width / 2) - (textboxWidth / 2), (height / 2) - (textboxHeight / 2), textboxWidth, textboxHeight), 5)

            filenameRender = font.render(fileName + ".leveldata", True, (0,0,0))
            displayRender = font.render(actionType, True, (0,0,0))
            screen.blit(displayRender, displayRender.get_rect(center = (width / 2, (height / 2) - 50)))
            screen.blit(filenameRender, filenameRender.get_rect(center = screen.get_rect().center))
        pygame.display.flip()
        pygame.display.update()