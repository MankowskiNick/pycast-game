
import pygame, sys, math
import Sprites, NPC
from pygame.locals import *
from Sprites import *
from genericpath import exists

#Create an empty map
def createEmptyMap():
    #Define map size
    mWidth = 50
    mHeight = 50

    #Declare empty map variable
    currentMap = []

    #Fill map with empty space
    for y in range(0,mHeight):
        temp = []
        for x in range(0,mWidth):
            temp.append(0)
        currentMap.append(temp)

    #Create walls for a border
    for y in range(0, mHeight):
        currentMap[y][0] = 1
        currentMap[y][mWidth - 1] = 1
    for x in range(0, mWidth):
        currentMap[0][x] = 1
        currentMap[mHeight - 1][x] = 1
    
    return currentMap

def updateSpawnLocation(player, level):
    for x in range(0, len(level[0])):
        for y in range(0, len(level)):
            if (level[y][x] == -1):
                level[y][x] = 0
    level[int(player.y)][int(player.x)] = -1

    return level

#Given coords and blocksize calculate where the coords are on the map
def getMapCoords(mCoords, blockSize):
    mx, my = mCoords
    mapX = (mx / blockSize)
    mapY = (my / blockSize)
    return mapX, mapY

#Draw the map information to the screen
def drawOverlay(px, py, screen, blockSize, npcList, drawMap, mapSpriteList):

    #Draw walls to the screen
    for x in range(0,len(drawMap[0])):
        for y in range(0,len(drawMap)):
            if (drawMap[y][x] > 0 and drawMap[y][x] <= 999):screen.blit(mapSpriteList[drawMap[y][x]], (x * blockSize, y * blockSize))
            elif (drawMap[y][x] == -1):     pygame.draw.circle(screen, (255, 0, 0),((x + 0.5) * blockSize, (y + 0.5) * blockSize), 3)
            else:pygame.draw.rect(screen, (255,255,255), pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize), 2)
    
    #Draw objects to the screen
    for i in range(0,len(npcList)):
        if npcList[i].type > 999:
            screen.blit(mapSpriteList[npcList[i].type], ((npcList[i].x - 0.5) * blockSize, (npcList[i].y - 0.5) * blockSize))
    
    #Draw a circle where the player is
    pygame.draw.circle(screen, (0,0,255),(px * blockSize, py * blockSize), 3)

def drawIcons(height, spriteLookUpTable, mapSpriteList, search_for_click, mouseX, mouseY, screen, currentBlockID):   
        #Render the sprites at the side of the screen & if necessary check which box was clicked and select the according sprite
        yCheck = int((height)  / (mapSpriteList[spriteLookUpTable[0]].get_height()*2)) * mapSpriteList[spriteLookUpTable[0]].get_height() * 2
        for i in range(0,len(spriteLookUpTable)):
            xDisplacement = 0
            yDisplacement = i * mapSpriteList[spriteLookUpTable[0]].get_height() * 2
            while yDisplacement >= yCheck:
                xDisplacement += mapSpriteList[spriteLookUpTable[0]].get_width() * 2
                yDisplacement -= yCheck
            if search_for_click:
                if mouseX > xDisplacement + height and mouseX < xDisplacement + height + mapSpriteList[spriteLookUpTable[i]].get_width()*2 and mouseY > yDisplacement and mouseY < yDisplacement + mapSpriteList[spriteLookUpTable[i]].get_width()*2:
                    currentBlockID = spriteLookUpTable[i]
            screen.blit(pygame.transform.scale(mapSpriteList[spriteLookUpTable[i]], (mapSpriteList[spriteLookUpTable[0]].get_width() * 2, mapSpriteList[spriteLookUpTable[0]].get_height() * 2)), (xDisplacement + height, yDisplacement))
            if (spriteLookUpTable[i] == currentBlockID):
                pygame.draw.rect(screen, (0,255,0), (xDisplacement + height, yDisplacement, mapSpriteList[spriteLookUpTable[i]].get_width()*2, 2))
                pygame.draw.rect(screen, (0,255,0), (xDisplacement + height, yDisplacement, 2, mapSpriteList[spriteLookUpTable[i]].get_height()*2))
                pygame.draw.rect(screen, (0,255,0), (xDisplacement + height + mapSpriteList[spriteLookUpTable[i]].get_width()*2 - 2, yDisplacement, 2, mapSpriteList[spriteLookUpTable[i]].get_height()*2))
                pygame.draw.rect(screen, (0,255,0), (xDisplacement + height, yDisplacement + mapSpriteList[spriteLookUpTable[i]].get_width()*2 - 2, mapSpriteList[spriteLookUpTable[i]].get_width()*2, 2))
        return currentBlockID

def drawTextBox(screen, width, height, textboxWidth, textboxHeight, font, fileName, actionType):
    pygame.draw.rect(screen, (255,255,255), ((width / 2) - (textboxWidth / 2), (height / 2) - (textboxHeight / 2), textboxWidth, textboxHeight))
    pygame.draw.rect(screen, (128,128,128), ((width / 2) - (textboxWidth / 2), (height / 2) - (textboxHeight / 2), textboxWidth, textboxHeight), 5)

    filenameRender = font.render(fileName + ".leveldata", True, (0,0,0))
    displayRender = font.render(actionType, True, (0,0,0))
    screen.blit(displayRender, displayRender.get_rect(center = (width / 2, (height / 2) - 50)))
    screen.blit(filenameRender, filenameRender.get_rect(center = screen.get_rect().center))
        
#Get the length in pixels of 1 unit
def getBlocksize(mWidth, mHeight, width, height):
    if (width / mWidth > height / mHeight):
        bSize = height / mHeight
    else:
        bSize = width / mWidth
    return bSize

#Get map dimensions
def getMapDimensions(drawMap):
    return len(drawMap[0]), len(drawMap)

def saveMap(drawMap, fileName, npcList, px, py):

    #Change write style depending on if the file exists or not
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

    #If the file exists
    if (exists(fileName)):
        loadMap = []
        file = open(fileName)
        fileLines = []
        fileLines = file.readlines()
        currentParser = 0
        mWidth = int(fileLines[0][0:2])
        mHeight = int(fileLines[0][3:5])
        
        #Parse through level data and store information in loadMap list
        for y in range(1,mHeight + 1):
            temp = []
            currentParser = 0
            for x in range(0,mWidth):
                oldParser = currentParser
                currentParser = fileLines[y].find(" ", oldParser + 1, len(fileLines[y]))
                temp.append(int(fileLines[y][oldParser:currentParser]))
            loadMap.append(temp)
        file.close()

        #Define a new NPCList given the map
        npcList = NPC.findNPC(loadMap)

        return loadMap, npcList, True, mWidth, mHeight
    
    #If the file doesn't exist
    else:
        print("File not found.")
        return [], [], False, 0, 0

def Main(player, currentMap, npcList, levelHIR):
    px, py = player.x, player.y
    pygame.init()

    width, height = (800, 600)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Map Generator")

    #Create new font for rendering textboxes
    font = pygame.font.Font(None, 30)

    #Define colors
    black = (0,0,0)
    white = (255,255,255)
    gray = (100,100,100)
    red = (255,0,0)
    blue = (0,0,255)

    #Define height and width of the currently viewed map
    mapWidth, mapHeight = len(currentMap[0]), len(currentMap)

    #Define the currently selected block
    currentBlockID = 1

    #Create a sprite list to reference for rendering
    mapSpriteList = createSpriteList()

    #Create list of integers that represent the keys for lookup of our spritelist
    spriteLookUpTable = list(mapSpriteList.keys())

    #Define the block size used in the renderer
    blockSize = getBlocksize(mapWidth, mapHeight, width, height)

    #Resize sprites to blocksize
    for i in range(0,len(spriteLookUpTable)):
        mapSpriteList[spriteLookUpTable[i]] = pygame.transform.scale(mapSpriteList[spriteLookUpTable[i]],(blockSize, blockSize))

    #Create text box things
    currentlyTyping = False
    fileName = ""
    actionType = ""
    textboxWidth, textboxHeight = 500,200

    #Determine whether process that draws sprites to screen should look where the cursor is as well
    mouseX, mouseY = 0,0
    search_for_click = False

    #Set the repeat for keylisteners back to default, so typing is possible
    pygame.key.set_repeat()

    while True:
        
        #Fill the screen with black to draw over the last frame
        screen.fill(black)

        for event in pygame.event.get():

            #Quit if you exit the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            #Key pressed event
            if event.type == KEYDOWN:
                
                #Is the user typing? If so handle input to the textbox
                if currentlyTyping:
                    if event.key == K_BACKSPACE:
                        fileName = fileName[:-1]

                    #Perform functions dealing with file management
                    elif event.key == K_RETURN:

                        #Saving file
                        if actionType == "Save file: ":
                            saveMap(currentMap, fileName, npcList, px, py)

                        #Opening file
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

                        #Reset things to stop typing
                        currentlyTyping = False
                        fileName = ""
                    
                    #Add character typed to filename
                    else:
                         fileName += event.unicode
                
                #Quit event
                elif event.key == K_q or event.key == K_ESCAPE:
                    return currentMap, npcList

                #Save file event
                elif event.key == K_s:
                    currentlyTyping = True
                    actionType = "Save file: "

                #Open file event
                elif event.key == K_o:
                    currentlyTyping = True
                    actionType = "Open file: "
                
                #Export file to python event
                elif event.key == K_e:
                    currentlyTyping = True
                    actionType = "Export file: "
                
                #New map creation event
                elif event.key == K_n:
                    currentMap = createEmptyMap()
                    npcList = []
                    mapWidth, mapHeight = getMapDimensions(currentMap)
                    blockSize = getBlocksize(mapWidth, mapHeight, width, height)
                    for i in range(0,len(spriteLookUpTable)):
                        mapSpriteList[spriteLookUpTable[i]] = pygame.transform.scale(mapSpriteList[spriteLookUpTable[i]], (blockSize, blockSize))
                                
                elif event.key == K_u:
                    currentMap = updateSpawnLocation(player, currentMap)
                
                #Keyboard input for selecting the given tile
                for i in range(0,9):
                    if event.key == i + 49:
                        if (i < len(spriteLookUpTable)):
                            currentBlockID = spriteLookUpTable[i]
            
            #Get the status of all mouse buttons
            mouseAction = pygame.mouse.get_pressed()

            #Define where on the map coord system the mouse is
            mapX, mapY = getMapCoords(pygame.mouse.get_pos(), blockSize)

            #If the left mouse button is currently pressed
            if (mouseAction[0]):

                #Limiter for placing two entities in one mouse click/on top of each other
                canPlace = True
                for i in range(0,len(npcList)):
                    if (mapX == int(npcList[i].x) and mapY == int(npcList[i].y)):
                        canPlace = False

                #Is the mouse clicking in the bound of the map?
                if mapX < len(currentMap[0]) and mapX >= 0 and mapY < len(currentMap) and mapY >= 0:
                    #Are we not placing an entity on top of another?
                    if canPlace:
                        if currentBlockID < 1000:
                            currentMap[mapY][mapX] = currentBlockID
                        elif currentBlockID < 2000:
                            npcList.append(NPC.NPC((mapX, mapY), currentBlockID, len(npcList), 100))
                            currentMap[mapY][mapX] = currentBlockID
                        elif currentBlockID > 1999:
                            npcList.append(NPC.NPC((mapX, mapY), currentBlockID, len(npcList), 100))
                            npcList[len(npcList) - 1].giveHIR(levelHIR, player, currentMap)
                
                #If the map is out of bounds, check to see if we are selecting a new tile
                else:
                    search_for_click = True
                    mouseX, mouseY = pygame.mouse.get_pos()

            #If the right mouse button is currently pressed
            if (mouseAction[2]):

                #If the mouse is in the bounds of the map
                if (mapX < len(currentMap[0]) and mapX >= 0 and mapY < len(currentMap) and mapY >= 0):
                    
                    #Remove NPC closest
                    for npc in npcList:
                        if math.pow(math.pow(mapX - npc.x, 2) + math.pow(mapY - npc.y, 2), 0.5) < 0.5:
                            npcList.remove(npc)
                            for n in range(0,len(npcList)):
                                npcList[n].updateLabel(n)
                            break
                    
                    #Set the current map value to zero(erase blocks and objects)
                    currentMap[int(mapY)][int(mapX)] = 0
        
        #Draw the options for different blocks and return the value if one is clicked
        currentBlockID = drawIcons(height, spriteLookUpTable, mapSpriteList, search_for_click, mouseX, mouseY, screen, currentBlockID)
        
        #Draw map to the screen
        drawOverlay(px, py, screen, blockSize, npcList, currentMap, mapSpriteList)

        #If the textbox is active, draw it
        if currentlyTyping:
            drawTextBox(screen, width, height, textboxWidth, textboxHeight, font, fileName, actionType)
        
        #Update screen
        pygame.draw.circle(screen, (150,150,150), (pygame.mouse.get_pos()), 5)
        pygame.display.flip()
        pygame.display.update()
