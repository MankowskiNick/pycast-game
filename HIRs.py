import sys
class HIRs:
    def __init__(self, level):
        #hallwayCount = 0
        #roomCount = 0 
        #Ultimately I want this to be what we can access
        self.rooms = []
        self.intersections = []
        self.halls = []

        self.level = level

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
        roomPath = self.generateRoomPath(enemy.coords, player, [])[0]
        print(roomPath)
        if len(roomPath) == 1:
            maze = self.getMaze((enemy.x, enemy.y), roomPath[0], roomPath[0])
        else:
            maze = self.getMaze((enemy.x, enemy.y), roomPath[0], roomPath[0])
            #maze += self.getMaze((8, 6), 1, 0)
            #print(self.rooms[roomPath[1-1]].getIntersectionCoords(roomPath[2-1]))
        if len(roomPath) > 1:
            for i in range(2,len(roomPath)):
                maze += self.getMaze(self.rooms[roomPath[i-2]].getIntersectionCoords(roomPath[i-1]), roomPath[i-1], roomPath[i])
            #print(maze)


    #Generate a path of rooms to go to
    def generateRoomPath(self, coords, player, path):
        #print(self.getRoom(player.x, player.y))
        playerRoom = self.getRoom(player.x, player.y)
        enemyRoom = self.getRoom(coords[0], coords[1])
        print("Player room: ", str(playerRoom))
        print("Enemy room: ", str(enemyRoom))

        path.append(enemyRoom)

        #Base case
        if playerRoom == enemyRoom:
            #path.append(enemyRoom)
            return path, True
        #Recursive case
        else:
            for possibleRoom in self.rooms[enemyRoom].connections:
                print("Possible options: ", str(self.rooms[enemyRoom].connections))
                print("Setting up coords (", str(self.rooms[possibleRoom].coords[0]), ",", str(self.rooms[possibleRoom].coords[1]), ")")
                path, result = self.generateRoomPath(self.rooms[possibleRoom].coords, player, path)
                if result:
                    #path.append(possibleRoom)
                    break
            return path, result


    #fix this lol
    def getMaze(self, startCoords, startRoom, endRoom):
        resolution = 50
        maze = [[int(startCoords[0]), int(startCoords[1])]]
        print("StartRoom: ", str(startRoom))
        print("EndRoom: ", str(endRoom))
        print("StartCoords: ", str(startCoords))
        targetX, targetY = self.rooms[startRoom].getIntersectionCoords(endRoom)[0], self.rooms[startRoom].getIntersectionCoords(endRoom)[1]
        currentX, currentY = startCoords
        startX, startY = startCoords
        stepX, stepY = (targetX - startX) / resolution, (targetY - startY) / resolution
        for i in range(0,resolution):
            present = False
            for coord in maze:
                if coord == [int(currentX), int(currentY)]:
                    present = True
            if not present:
                for i in range(-1,2):
                    for j in range(-1, 2):
                        if (self.level[int(currentY) + j][int(currentX) + i] == 0) or (self.level[int(currentY) + j][int(currentX) + i] >= 2000) or (self.level[int(currentY) + j][int(currentX) + i] == 999): 
                            maze.append([int(currentX) + i, int(currentY) + j])
                            self.level[int(currentY) + j][int(currentX) + i] = 999
            currentX += stepX
            currentY += stepY
        return maze
                  
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
        return self.coords