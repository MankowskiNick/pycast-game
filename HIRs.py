import sys
class HIRs:
    def __init__(self, level):
        #hallwayCount = 0
        #roomCount = 0 
        #Ultimately I want this to be what we can access
        self.rooms = []
        self.intersections = []
        self.halls = []

        levelWidth = len(level[0])
        levelHeight = len(level)

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
                    print("Newly completed space")
                    print("    -Coords: ", str((x, y)))
                    print("    -Size: ", str(width), "x", str(height))
                    print(" ")
                    
                    perimeterCoords = []

                    #TEMP - Place marker
                    level[y][x] = 996

                    #Calculate the perimeter coords
                    perimeterCoords = self.findPerimeter(x, y, width, height)
                    
                    #create new room object
                    self.rooms.append(Room([x,y], [width, height], perimeterCoords, currentCoordList))
        '''
        #Find all possible intersections
        intersectionCoords = []
        for i in range(0,len(self.rooms)):
            for j in range(0,len(self.rooms)):
                if not (i == j):
                    intersectionCoords += self.calculateIntersect(self.rooms[i], self.rooms[j], level)
                    for n in range(0,len(intersectionCoords)):
                        #self.intersections.append(Intersection(intersectionCoords[n], [i, j]))
                        print("New intersection found.\n    Coords: (", str(intersectionCoords[n][0]), " , ", str(intersectionCoords[n][1]), ")\n")
                        level[intersectionCoords[n][1]][intersectionCoords[n][0]] = 998 #TEMP - place marker
        
        #Remove duplicates
        for n in range(0, len(intersectionCoords)):
            cullList, level = self.removeDuplicates(intersectionCoords[n][0], intersectionCoords[n][1], level)
            for k in range(0, len(cullList)):
                if (cullList[k] == intersectionCoords[n]):
                    intersectionCoords.remove[intersectionCoords[n]]
        for n in range(0, len(intersectionCoords)):
            self.intersections.append(Intersection(intersectionCoords[n]))#, [i, j]))
        '''
        self.level = level #TEMP map - we use to show indicators of where things are
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

    def calculateIntersect(self, room1, room2, level):
        intersectionPoints = []
        perimeter1 = room1.perimeterCoords
        perimeter2 = room2.perimeterCoords
        for i in range(0, len(room1.perimeterCoords)):
            for j in range(0, len(room2.perimeterCoords)):
                if (room1.perimeterCoords[i] == room2.perimeterCoords[j] and level[room1.perimeterCoords[i][1]][room1.perimeterCoords[i][0]] == 0):
                    intersectionPoints.append(room1.perimeterCoords[i])
        for i in range(0, len(room1.coordList)):
            for j in range(0, len(room2.coordList)):
                if (room1.coordList[i] == room2.coordList[j]):
                    intersectionPoints.append(room1.coordList[i])

        return intersectionPoints

    def removeDuplicates(self, x, y, level):
        cullList = []
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if (i >= 0 and j >= 0 and i < len(level[0]) and j < len(level)) and not (i == x and j == y):
                    if (level[j][i] > 995 and level[j][i] <= 999):
                        level[j][i] = 0
                        cullList.append([i,j])
                        return self.removeDuplicates(i, j, level), level
        level[y][x] = 998
        return cullList, level
        
class Room:
    #Coordinates are a list given in terms of the top left tile, size is a list in terms of [width, height]
    def __init__(self, coords, size, perimeterCoords, coordList):
        self.coords = coords
        self.size = size
        self.perimeterCoords = perimeterCoords
        self.coordList = coordList

class Intersection:

    #Coordinates are a list given in terms of the top left tile, connections are what hallways/rooms the intesection is connecting and is in a list
    def __init__(self, coords):#, connections):
        self.coords = coords
        #self.connections = connections