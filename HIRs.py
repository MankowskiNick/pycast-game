import sys, pdb
class HIRs:
    def __init__(self, level):
        #hallwayCount = 0
        #roomCount = 0 
        #Ultimately I want this to be what we can access
        self.rooms = []
        self.intersections = []
        self.halls = []

        self.level = level

        self.path = []

        levelWidth = len(self.level[0])
        levelHeight = len(self.level)

        listChecked = [[0,0]]
 
        #Scan the entire level
        for x in range(0,levelWidth):
            for y in range(0,levelHeight):
                alreadyChecked = False

                for coords in listChecked:
                    
                    if coords == [x,y]:
                        alreadyChecked = True

                if not alreadyChecked and (level[y][x] == 0 or level[y][x] >= 1000):
                    print("New space found.  Starting coords: ", str((x,y)), " Level value: ", str(level[y][x]))
                    doneExpanding = False
                    currentBox = [x,y]
                    width, height = 1 , 1
                    addWidth = True
                    counter = 0
                    while not doneExpanding:
                        success, tmpBox, tmpWidth, tmpHeight, newlyCheckedCoords, tmpCoords = self.expand(currentBox, width, height, addWidth, level)
                        if success: 
                            counter = 0
                            currentBox = tmpBox
                            width, height = tmpWidth, tmpHeight
                            currentCoordList = tmpCoords
                        else:
                            if counter < 5:
                                counter += 1
                            else:
                                doneExpanding = True
                        if addWidth:
                            addWidth = False
                        else: 
                            addWidth = True
                        for c in newlyCheckedCoords:
                            listChecked.append(c)

                    
                    perimeterCoords = []

                    #self.level[y][x] = 996 #TEMP - Place marker

                    #Calculate the perimeter coords
                    perimeterCoords = self.findPerimeter(x, y, width, height)
                    
                    #create new room object
                    self.rooms.append(Room([x,y], [width, height], perimeterCoords, currentCoordList, len(self.rooms)))
                    print("Completed space")
                    print("    -ID: ", str(len(self.rooms) - 1))
                    print("    -Coords: ", str((x, y)))
                    print("    -Size: ", str(width), "x", str(height))
                    print(" ")

        #Find all possible intersections
        intersectionCoords = []
        intersectionConnections = []
        for i in range(0,len(self.rooms)):
            for j in range(0,len(self.rooms)):
                if not (i == j):
                    newIntersectionCoords = self.calculateIntersect(self.rooms[i], self.rooms[j], level, intersectionCoords)
                    if (len(newIntersectionCoords) > 0):
                        newIntersectionConnections = [i,j] #room 1 value, room 2 value
                        for n in range(0,len(newIntersectionCoords)):
                            print("New intersection found.\n    Coords: (", str(newIntersectionCoords[n][0]), " , ", str(newIntersectionCoords[n][1]), ")")
                        intersectionCoords += newIntersectionCoords
                        intersectionConnections.append(newIntersectionConnections)
                        print("    Links:", str(newIntersectionConnections),"\n")

        #Remove intersections that spawn next to eachother
        for n in range(0, len(intersectionCoords)):
            if n < len(intersectionCoords):
                cullList = self.removeDuplicates(intersectionCoords[n][0], intersectionCoords[n][1], [], intersectionCoords)
                for k in range(0, len(cullList)):
                    if (cullList[k] == intersectionCoords[n]):
                        intersectionCoords.remove(intersectionCoords[n])
        
        #Link rooms
        print("Linking rooms...")
        for n in range(0, len(intersectionCoords)):
            #level[intersectionCoords[n][1]][intersectionCoords[n][0]] = 998  #TEMP - PLACE MARKER
            self.rooms[intersectionConnections[n][0]].linkRoom(intersectionConnections[n][1], intersectionCoords[n])
            self.rooms[intersectionConnections[n][1]].linkRoom(intersectionConnections[n][0], intersectionCoords[n])
        
        #Display linker info
        for room in self.rooms:
            print("Room ID: ", str(room.id), "\n    -Coords: (", str(room.coords[0]), " , ", str(room.coords[1]), ")\n  -Links: ", str(room.connections))
        
        #self.level = level #TEMP map - we use to show indicators of where things are
        print("HIRs model created.")

    def expand(self, currentBox, width, height, addWidth, level):
        checkedCoords = []
        
        #unpack values from currentBox
        left, top = currentBox[0], currentBox[1]
        if addWidth:

            width += 1

            box = [left, top]
            #check box
            boxSuccess = True
            for i in range(0,width):
                for j in range(0,height):
                    x = i + box[0]
                    y = j + box[1]
                    checkedCoords.append([x, y])
                    if level[y][x] > 0 and level[y][x] < 1000:
                        boxSuccess = False
                    else:
                        level[y][x] == 5
            if boxSuccess:
                return True, box, width, height, checkedCoords, checkedCoords
        else:

            height += 1
            
            box = [left, top]

            #check box
            boxSuccess = True
            for i in range(0,width):
                for j in range(0,height):
                    x = i + box[0]
                    y = j + box[1]
                    checkedCoords.append([x, y])
                    if level[y][x] > 0 and level[y][x] < 1000:
                        boxSuccess = False
                    else:
                        level[y][x] == 5
            if boxSuccess:
                return True, box, width, height, checkedCoords, checkedCoords

        return False, [], 0, 0, checkedCoords, []

    def findPerimeter(self, x,y,width,height):
        perimeterCoords = []

        #Add tiles on the horizontal sides
        for i in range(0, width):
            perimeterCoords.append([x + i, y - 1])
            perimeterCoords.append([x + i, y + height])

        #Add tiles on the vertical sides
        for i in range(0, height):
            perimeterCoords.append([x - 1, y + i])
            perimeterCoords.append([x + width, y + i])

        return perimeterCoords

    def calculateIntersect(self, room1, room2, level, intersectCoords):
        intersectionPoints = []
        perimeter1 = room1.perimeterCoords
        perimeter2 = room2.perimeterCoords
        
        #Check perimeters
        for i in range(0, len(room1.perimeterCoords)):
            for j in range(0, len(room2.perimeterCoords)):
                if (room1.perimeterCoords[i] == room2.perimeterCoords[j] and level[room1.perimeterCoords[i][1]][room1.perimeterCoords[i][0]] == 0):
                    intersectionPoints.append(room1.perimeterCoords[i])
        
        #Check interior points
        for i in range(0, len(room1.coordList)):
            for j in range(0, len(room2.coordList)):
                if (room1.coordList[i] == room2.coordList[j]):
                    intersectionPoints.append(room1.coordList[i])
        
        #Don't add intersections we have already counted, ensure we haven't already counted these ones.
        #If we don't add this, it will double count every intersection
        for n in range(0,len(intersectionPoints)):
            for k in range(0,len(intersectCoords)):
                if n < len(intersectionPoints):
                    if (intersectionPoints[n] == intersectCoords[k]):
                        intersectionPoints.remove(intersectionPoints[n])
                        #break
        return intersectionPoints

    def removeDuplicates(self, x, y, cullList, intersectCoords):
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                for n in range(0, len(intersectCoords)):
                    foundCoord = False
                    for k in range(0, len(cullList)):
                        if (cullList[k] == [i, j]):
                            foundCoord = True
                    if (not foundCoord) and ([i,j] == intersectCoords[n]) and not (i == x and j == y):
                        cullList.append([i,j])
                        cullList.append(self.removeDuplicates(i, j, cullList, intersectCoords))
        return cullList

    def getRoom(self, x, y):
        for room in self.rooms:
            for coords in room.coordList:
                if ([int(x), int(y)] == coords):
                    return room.id 
            for coords in room.perimeterCoords:
                if ([int(x), int(y)] == coords):
                    return room.id 

    def pathfind(self, enemy, player, level):
        roomPath = [self.getRoom(enemy.coords[0], enemy.coords[1])]
        tmp, tmpRoomPath = self.generateRoomPath(enemy.coords, player, [])
        roomPath += tmpRoomPath

        #print(roomPath)
        if (len(roomPath) > 1):
            phantomList = self.getMaze(roomPath, 1, [[self.rooms[roomPath[0]].getIntersectionCoords(self.rooms[roomPath[1]].id)[0], self.rooms[roomPath[0]].getIntersectionCoords(self.rooms[roomPath[1]].id)[1]]])
        #for i in self.phantomList:
        #    self.level[i[1]][i[0]] = 999

        return phantomList
            

    #Generate a path of rooms to go to
    def generateRoomPath(self, coords, player, path):
        playerRoom = self.getRoom(player.x, player.y)
        enemyRoom = self.getRoom(coords[0], coords[1])
        if (playerRoom == enemyRoom):
            return True, path
        else:
            for room in self.rooms[enemyRoom].connections:
                for checkRoom in path:
                    if checkRoom == room:
                        return False, path
                path.append(room)
                result, tmpPath = self.generateRoomPath(self.rooms[room].coords, player, path)
                if result:
                    path = tmpPath
                    return True, path
                else:
                    path.remove(room)
        return False, path

    def getMaze(self, roomPath, pos, phantomList):
        resolution = 3
        if (pos == len(roomPath)):
            return phantomList
        else:
            if (pos + 1 < len(roomPath)):
                coord1 = self.rooms[roomPath[pos - 1]].getIntersectionCoords(roomPath[pos])
                coord2 = self.rooms[roomPath[pos]].getIntersectionCoords(roomPath[pos + 1])

                #print(coord1, coord2)
                currentX, currentY = coord1[0], coord1[1]
                stepX, stepY = (coord2[0] - coord1[0]) / resolution, (coord2[1] - coord1[1]) / resolution
                for i in range(0,resolution):
                    currentX += stepX
                    currentY += stepY
                    if (self.level[int(currentY)][int(currentX)] == 0 or self.level[int(currentY)][int(currentX)] >= 2000):
                        #self.level[int(currentY)][int(currentX)] = 999
                        #phantomList.append(Phantom(int(currentX), int(currentY)))
                        phantomList.append([int(currentX), int(currentY)])

            return self.getMaze(roomPath, pos + 1, phantomList)
                  
class Room:
    #Coordinates are a list given in terms of the top left tile, size is a list in terms of [width, height]
    def __init__(self, coords, size, perimeterCoords, coordList, id):
        self.coords = coords
        self.size = size
        self.perimeterCoords = perimeterCoords
        self.coordList = coordList
        self.id = id
        self.connections = []
        self.intersectionCoords = []
    #Link rooms
    def linkRoom(self, roomID, coords):
        self.connections.append(roomID)
        self.intersectionCoords.append(coords)
    def getIntersectionCoords(self, searchTerm):
        for i in range(0,len(self.connections)):
            if self.connections[i] == searchTerm:
                return self.intersectionCoords[i]
        return [0,0]