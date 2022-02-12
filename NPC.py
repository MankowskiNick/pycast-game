import math, sys

#Find NPCs and create database of them along with coords
def findNPC(focusMap):                                         
	npcList = []
	for x in range(0,len(focusMap[0])):
		for y in range(0,len(focusMap)):
			if focusMap[y][x] > 999 and focusMap[y][x] < 2000:
				npcList.append(NPC((x, y), focusMap[y][x], len(npcList), 100))
			if focusMap[y][x] > 1999:
				npcList.append(NPC((x, y), focusMap[y][x], len(npcList), 100))
				focusMap[y][x] = 0
			else:
				continue
	return npcList

class NPC:
	def __init__(self, coords, type, label, hp):
		
		#Define coords
		self.coords = coords
		self.x, self.y = coords

		self.startX, self.startY = coords
		self.angle = 0

		#Adjust coords
		self.x += 0.5
		self.y += 0.5

		#Define type
		self.type = type

		self.frameCounter = 0

		#Define if NPC is static object or actual npc
		if (self.type < 2000):
			self.isObject = True
		else:
			self.isObject = False

		#Define whether or not person is dead
		if self.type >= 3000 or self.isObject:
			self.isAlive = False
		else:
			self.isAlive = True

		#Define label, position in the npcList array that this npc lies
		self.label = label

		#Define step size
		self.stepSize = 0.01

		self.xDisp = 0
		self.yDisp = 0

		self.hp = hp

		self.path = []
		self.pathPos = 0

		#Define npc as not active, npc hasnt been seen
		self.deActivate()

		#stored as [[x0,x1],[y0,y1]]
		self.updateHitBox()

	def walk(self, player, level, npcList, frameCount):
		self.coords = self.x, self.y
		if len(self.path) > 0:# and self.pathPos < len(self.path):
			xDist = self.path[self.pathPos][0] - self.x + 0.5
			yDist = self.path[self.pathPos][1] - self.y + 0.5
		else:
			xDist = player.x - self.x
			yDist = player.y - self.y
		distTo = math.sqrt(pow(xDist, 2) + pow(yDist, 2))
		if (self.isActive and (not self.isObject) and self.isAlive):
			
			#add counter and give like 5 frames before we can recount
			if (frameCount % len(npcList) == self.label and frameCount > self.frameCounter):
				self.frameCounter = frameCount + 50
			if frameCount >= self.frameCounter:
				if not self.HIR.getRoom(player.x, player.y) == self.HIR.getRoom(self.x, self.y):
					self.path = self.HIR.pathfind(self, player, level)
					#self.pathPos = 0
				else:
					self.path = []
					self.pathPos = 0

			

			self.xDisp = self.stepSize * xDist / distTo
			self.yDisp = self.stepSize * yDist / distTo
			#print(self.path)
			#print(self.pathPos, distTo)
			activateDist = 0.5
			tolerance = 0.05
			if (not self.wallDetect(level) and self.npcDetect(npcList) == False and distTo > activateDist):# and tolerance > activateDist - distTo):
				self.x += self.xDisp
				self.y += self.yDisp
			if (distTo < activateDist):
				self.x += self.xDisp
				self.y += self.yDisp
				self.pathPos+=1
				
			self.updateHitBox()

		if (not self.isObject and not self.isAlive and self.type >= 4000):
			if distTo < 0.3:
				self.activate(player)
				return True
		return False

	#rewrite this
	def wallDetect(self, level):
		if (level[int(self.y + self.yDisp)][int(self.x + self.xDisp)] > 0):
			if (level[int(self.y)][int(self.x + self.xDisp)] == 0):
				self.yDisp = 0
			elif (level[int(self.y + self.yDisp)][int(self.x)] == 0):
				self.xDisp = 0
			#else:
				#return True
			return False
		return False

	def npcDetect(self, npcList):
		for i in range(0,len(npcList)):
			if (i != self.label):

				currentHitBox = npcList[i].hitBox

				minX = currentHitBox[0][0]
				maxX = currentHitBox[0][1]

				minY = currentHitBox[1][0]
				maxY = currentHitBox[1][1]

				k=3
				for n in range(0,k):
					currentAngle = n * k * math.pi / 180
					checkX = self.x + 0.3 * math.cos(currentAngle)
					checkY = self.y + 0.3 * math.sin(currentAngle)
					if (checkX >= minX and checkX <= maxX and checkY >= minY and checkY <= maxY):
						self.x -= self.stepSize * math.cos(currentAngle)
						self.y -= self.stepSize * math.sin(currentAngle)

						return True
		return False	

	def setActive(self):
		self.isActive = True

	def deActivate(self):
		self.isActive = False

	def die(self):
		self.isAlive = False
		self.type += 1000

	def updateHitBox(self):
		self.hitBox = [[self.x - 0.15, self.x + 0.15],[self.y - 0.15, self.y + 0.15]]
	
	def updateLabel(self, n):
		self.label = n

	def takeDamage(self, dmg):
		if self.isAlive:
			self.hp -= dmg
			if self.hp <= 0:
				self.die()
				return True
		return False
	
	def giveHIR(self, HIR, player, level):
		self.HIR = HIR
		self.path = self.HIR.pathfind(self, player, level)
		self.pathPos = 0
	#In the event the self object is a picup, activate whatever it is intended to do.
	def activate(self, player):
		if self.type < 4000:
			return
		else:
			if self.type == 4000:
				player.addHealth(15)
			elif self.type == 4001:
				player.addAmmo(12)
			elif self.type == 4002:
				player.addAmmo(4)

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
        phantomList = []
        if (len(roomPath) > 1):
            phantomList = self.getMaze(roomPath, 1, [[self.rooms[roomPath[0]].getIntersectionCoords(self.rooms[roomPath[1]].id)[0], self.rooms[roomPath[0]].getIntersectionCoords(self.rooms[roomPath[1]].id)[1]]])
        #for i in phantomList:
            #self.level[i[1]][i[0]] = 999
		
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
        resolution = 1
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