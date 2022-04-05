
import pygame, sys, math
import Sprites, NPC, Level
from pygame.locals import *
from Sprites import *
from genericpath import exists

#Create an empty map - this is not gonna work for a bit, ill come back to it
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
    wall_level = level.getWallMap()
    for x in range(0, len(level[0])):
        for y in range(0, len(level)):
            if (wall_level[y][x] == -1):
                wall_level[y][x] = 0
    wall_level[int(player.y)][int(player.x)] = -1
    level.setWallMap(wall_level)
    return level

#Given coords and blocksize calculate where the coords are on the map
def getMapCoords(mCoords, blockSize):
    mx, my = mCoords
    mapX = (mx / blockSize)
    mapY = (my / blockSize)
    return mapX, mapY

#Draw the map information to the screen
def drawOverlay(px, py, screen, blockSize, npcList, level, mapSpriteList):
    drawMap = level.getWallMap()
    #Draw walls to the screen
    for x in range(0,len(drawMap[0])):
        for y in range(0,len(drawMap)):
            if (drawMap[y][x] > 0 and drawMap[y][x] <= 999):screen.blit(mapSpriteList[drawMap[y][x]], (x * blockSize, y * blockSize))
            elif (drawMap[y][x] == -1):     pygame.draw.circle(screen, (255, 0, 0),((x + 0.5) * blockSize, (y + 0.5) * blockSize), 3)
            else:pygame.draw.rect(screen, (255,255,255), pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize), 2)
    #we will need to think of a way to draw floors and ceilings too
    #Draw objects to the screen
    for i in range(0,len(npcList)):
        if npcList[i].type > 999:
            screen.blit(mapSpriteList[npcList[i].type], ((npcList[i].x - 0.5) * blockSize, (npcList[i].y - 0.5) * blockSize))
    
    #Draw a circle where the player is
    pygame.draw.circle(screen, (0,0,255),(px * blockSize, py * blockSize), 3)

#Draw the selectable textures
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

#Draw text box for user input(this whole system could be way better and more object oriented, tbh)
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
def getMapDimensions(level):
    drawMap = level.getWallMap()
    return len(drawMap[0]), len(drawMap)

def saveMap(level, fileName, npcList, px, py):

    #Change write style depending on if the file exists or not
    if (exists("levels/" + fileName + ".leveldata")):
        file = open("levels/" + fileName + ".leveldata", "w")
    else:
        file = open("levels/" + fileName + ".leveldata", "x")

    floor_map = level.getFloorMap()
    wall_map = level.getWallMap()
    ceiling_map = level.getCeilingMap()

    #Add objects to wall_map
    for i in range(len(npcList)):
        wall_map[npcList[i].startY][npcList[i].startX] = npcList[i].type
    
    #Add player position to wall_map
    wall_map[int(px)][int(py)] = -1

    #Write map height data to first line of file
    if (len(wall_map[0]) > 9 and len(wall_map) > 9):
        file.write(str(len(wall_map[0])) + " " + str(len(wall_map)) + "\n")
    elif (len(wall_map[0] <= 9)):
        file.write("0" + str(len(wall_map[0])) + " " + str(len(wall_map)) + "\n")
    elif (len(wall_map) <= 9):
        file.write(str(len(wall_map[0])) + " 0" + str(len(wall_map)) + "\n")

    #Write all 3 maps to file, separated b
    for y in range(0,len(wall_map)):
        temp = ""
        for x in range(0,len(wall_map[y])):
            temp += (str(floor_map[y][x]) + "," + str(wall_map[y][x]) + "," + str(ceiling_map[y][x]) + " ")
        temp += "\n"
        file.write(temp)
    file.close()

def loadMapFromFile(fileName):

    #If the file exists
    if (exists(fileName)):
        floor_map = []
        wall_map = []
        ceiling_map = []

        file = open(fileName)
        fileLines = []
        fileLines = file.readlines()
        currentParser = 0
        mWidth = int(fileLines[0][0:2])
        mHeight = int(fileLines[0][3:5])
        
        #Parse through level data and store information in wall_map list
        for y in range(1,mHeight + 1):
            temp_floor = []
            temp_wall = []
            temp_ceiling = []
            currentParser = 0
            for x in range(0,mWidth):
                oldParser = currentParser
                currentParser = fileLines[y].find(" ", oldParser + 1, len(fileLines[y]))
                new_floor, new_wall, new_ceiling = fileLines[y][oldParser:currentParser].split(",")
                #new_floor, new_wall, new_ceiling = int(new_floor_str), int(new_wall_str), int(new_ceiling_str)
                temp_floor.append(int(new_floor))
                temp_wall.append(int(new_wall))
                temp_ceiling.append(int(new_ceiling))
                #temp.append(int(fileLines[y][oldParser:currentParser]))
            floor_map.append(temp_floor)
            wall_map.append(temp_wall)
            ceiling_map.append(temp_ceiling)

        file.close()

        #Define a new NPCList given the map
        npcList = NPC.findNPC(wall_map)

        level = Level.Level(floor_map, wall_map, ceiling_map)

        return level, npcList, True, mWidth, mHeight
    
    #If the file doesn't exist
    else:
        print("File not found.")

        level = Level.Level([], [], [])
        return level, [], False, 0, 0

def Main(player, level, npcList, levelHIR):
    px, py = player.x, player.y
    pygame.init()
    currentMap = level.getWallMap()

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
                            saveMap(level, fileName, npcList, px, py)

                        #Opening file
                        if actionType == "Open file: ":
                            tempMap, tempNPCList, fileExists, mapWidth, mapHeight = loadMapFromFile("levels/" + fileName + ".leveldata")
                            if (fileExists):
                                level = tempMap
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
                    level.setFloorMap(currentMap)
                    return level, npcList

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
                    '''
                    this isn't gonna work for a bit, ill come back to it
                    remember to unindent when uncommenting
                    #New map creation event
                    elif event.key == K_n:
                        currentMap = createEmptyMap()
                        npcList = []
                        mapWidth, mapHeight = getMapDimensions(currentMap)
                        blockSize = getBlocksize(mapWidth, mapHeight, width, height)
                        for i in range(0,len(spriteLookUpTable)):
                            mapSpriteList[spriteLookUpTable[i]] = pygame.transform.scale(mapSpriteList[spriteLookUpTable[i]], (blockSize, blockSize))
                    '''   
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
                            currentMap[int(mapY)][int(mapX)] = currentBlockID
                        elif currentBlockID < 2000:
                            npcList.append(NPC.NPC((mapX, mapY), currentBlockID, len(npcList), 100))
                            currentMap[int(mapY)][int(mapX)] = currentBlockID
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
        drawOverlay(px, py, screen, blockSize, npcList, level, mapSpriteList)

        #If the textbox is active, draw it
        if currentlyTyping:
            drawTextBox(screen, width, height, textboxWidth, textboxHeight, font, fileName, actionType)
        
        #Update screen
        pygame.draw.circle(screen, (150,150,150), (pygame.mouse.get_pos()), 5)
        pygame.display.flip()
        pygame.display.update()
