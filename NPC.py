import math, sys, random, pygame, Sound
from pygame.locals import *
from random import seed
from random import randint

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

#Return the list position of a door if the coords are near said door
def getDoor(doors, coords):
	for i in range(0, len(doors)):
		if math.sqrt(pow(doors[i].x + 0.5 - coords[0], 2) + pow(doors[i].y + 0.5 - coords[1], 2)) <= 0.8:
			return i
	return 0

class NPC:
	def __init__(self, coords, type, label, hp):

		#Set the sprite for the object
		
		#Type = Object
		if (type > 999 and type <= 1999):
			self.defaultSprite = pygame.image.load("assets/object/" + str(type) + ".png")
		
		#Type = NPC
		elif (type <= 2999):
			self.defaultSprite = pygame.image.load("assets/npc/" + str(type) + "/alive/default.png")
			self.deadSprite = pygame.image.load("assets/npc/" + str(type) + "/dead/default.png")
			self.walkSprites = [pygame.image.load("assets/npc/" + str(type) + "/alive/step1.png"), pygame.image.load("assets/npc/" + str(type) + "/alive/step2.png")]
			self.fireSprites = [pygame.image.load("assets/npc/" + str(type) + "/alive/fire1.png"), pygame.image.load("assets/npc/" + str(type) + "/alive/fire2.png"), pygame.image.load("assets/npc/" + str(type) + "/alive/fire3.png")]
			self.fireDict = [0,1,2,1,0]
		
		#Type = Dead NPC
		elif (type <= 3999):
			self.defaultSprite = pygame.image.load("assets/npc/" + str(type - 1000) + "/dead/default.png")
		
		#Type = Pickup
		elif (type <= 4999):
			self.defaultSprite = pygame.image.load("assets/pickup/" + str(type) + ".png")
		
		self.currentSprite = self.defaultSprite

		#Used for sprite animation things
		self.lastFrameChange = 0
		self.fireIndex = 0
		self.shooting = False
		self.canMove = True

		#Define coords
		self.coords = coords
		self.x, self.y = coords

		#Define the position that the NPC starts
		self.startX, self.startY = coords

		#Adjust coords to be in the center of a tile
		self.x += 0.5
		self.y += 0.5

		#Define type
		self.type = type

		#Set up variables used to time events
		self.frameCounter = 0
		self.lastFrameShot = 0

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
		self.stepSize = 0.015

		#Declare x & y displacement used for walking
		self.xDisp = 0
		self.yDisp = 0

		#Declare distance to player
		self.distToPlayer = 0

		#Declare health
		self.hp = hp
		
		#Set up path and a variable pointing to the position in the path that
		#the NPC currently is at
		self.path = []
		self.pathPos = 0

		#Define the weapon and after how many frames the enemy can shoot at the player
		self.weapon = NPCWeapon(25, 10, 12)
		self.shotDelay = 64

		#Define npc as not active, npc hasnt been seen
		self.deActivate()
		#self.setActive()
		
		#stored as [[x0,x1],[y0,y1]]
		self.updateHitBox()

	def walk(self, player, level, npcList, doors, frameCount):
		#Update the distance to the player
		self.distToPlayer = math.sqrt(pow(player.x - self.x, 2) + pow(player.y - self.y, 2))

		if (self.isActive and (not self.isObject) and self.isAlive):

			#Animate walking
			if (not self.shooting and self.lastFrameChange + 10 <= frameCount):
				if (self.currentSprite == self.walkSprites[0]):
					self.currentSprite = self.walkSprites[1]
				else:
					self.currentSprite = self.walkSprites[0]
				self.lastFrameChange = frameCount

			#Animate Shooting
			if (self.shooting and frameCount - self.lastFrameChange >= 2):
				self.fireIndex += 1
				if (self.fireIndex < len(self.fireDict)):
					self.currentSprite = self.fireSprites[self.fireDict[self.fireIndex]]
					self.lastFrameChange = frameCount
				else:
					self.currentSprite = self.defaultSprite
					self.shooting = False
					self.fireIndex = 0
					self.canMove = True
				
			#Take shot if shooting
			if frameCount >= self.lastFrameShot + self.shotDelay:
				seed(frameCount / 13 + player.x - self.hp * 987)
				self.lastFrameShot = frameCount
				chance = randint(0,100)
				if chance <= 40:
					self.weapon.Shoot(self, player, level, doors)
					Sound.Shoot_Sound(1)
					self.shooting = True
					self.lastFrameChange = frameCount
					self.currentSprite = self.fireSprites[self.fireDict[self.fireIndex]]
					self.canMove = False

		self.coords = self.x, self.y
		xDist = 1
		yDist = 1
		if len(self.path) > 0 and self.pathPos < len(self.path):
			xDist = self.path[self.pathPos][0] - self.x + 0.5
			yDist = self.path[self.pathPos][1] - self.y + 0.5
		else:
			xDist = player.x - self.x
			yDist = player.y - self.y
		
		distTo = math.sqrt(pow(xDist, 2) + pow(yDist, 2))
		self.wallDetect(level, doors)
		if (self.isActive and (not self.isObject) and self.isAlive and self.distToPlayer > 0.5):
			
			#add counter and give like 5 frames before we can recount
			if (frameCount % len(npcList) == self.label and frameCount > self.frameCounter):
				self.frameCounter = frameCount + 100
			if frameCount >= self.frameCounter:
				if not self.HIR.getRoom(player.x, player.y) == self.HIR.getRoom(self.x, self.y):
					self.path = self.HIR.pathfind(self, player, level)
					self.pathPos = 0
				else:
					self.path = []
					self.pathPos = 0

			

			self.xDisp = self.stepSize * xDist / distTo
			self.yDisp = self.stepSize * yDist / distTo
			activateDist = 0.5

			if (not self.wallDetect(level, doors) and self.npcDetect(npcList) == False and distTo > activateDist and self.canMove):
				self.x += self.xDisp
				self.y += self.yDisp
			if (distTo < activateDist):
				self.x += self.xDisp
				self.y += self.yDisp
				self.pathPos+=1
				
			self.updateHitBox()

		if (self.type >= 4000):
			if self.distToPlayer < 0.5:
				return self.activate(player)
		return False

	def wallDetect(self, level, doors):
		doorID = getDoor(doors, [self.x + self.xDisp, self.y + self.yDisp])
		
		if (level[int(self.y + self.yDisp)][int(self.x + self.xDisp)] > 0 and level[int(self.y + self.yDisp)][int(self.x + self.xDisp)] <= 899) or (level[int(self.y + self.yDisp)][int(self.x + self.xDisp)] > 899 and level[int(self.y + self.yDisp)][int(self.x + self.xDisp)] <= 999 and (not doors[doorID].isOpen) and (not doorID == 0)):
			doorID = getDoor(doors, [self.x + self.xDisp, self.y + self.y + self.yDisp])
			if (level[int(self.y)][int(self.x + self.xDisp)] == 0) or (level[int(self.y)][int(self.x + self.xDisp)] > 899 and level[int(self.y)][int(self.x + self.xDisp)] <= 999 and (doors[doorID].isOpen) and (not doorID == 0)):
				self.yDisp = 0
			elif (level[int(self.y + self.yDisp)][int(self.x)] == 0) or (level[int(self.y + self.yDisp)][int(self.x)] > 899 and level[int(self.y + self.yDisp)][int(self.x)] <= 999 and (doors[doorID].isOpen) and (not doorID == 0)):
				self.xDisp = 0
		return False

	def npcDetect(self, npcList):
		for npc in npcList:
			if (not npc == self) and npc.isAlive:
				distTo = math.sqrt(pow(self.x - npc.x, 2) + pow(self.y - npc.y, 2))
				if (distTo < 0.3 and npc.x - self.x != 0):
					currentAngle = math.atan((npc.y - self.y) / (npc.x - self.x))
					self.x -= self.stepSize * (npc.x - self.x)
					self.y -= self.stepSize * (npc.y - self.y)
					return True

		return False	

	def setActive(self):
		self.isActive = True

	def deActivate(self):
		self.isActive = False

	def die(self):
		self.isAlive = False
		self.type += 1000
		self.currentSprite = self.deadSprite

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
	
	#In the event the self object is a pickup, activate whatever it is intended to do.
	def activate(self, player):
		if self.type < 4000:
			return False
		else:
			#Sound.Pickup_Sound(self.type)
			if self.type == 4000:
				return player.addHealth(15)
			elif self.type == 4001:
				player.addAmmo(12)
				return True
			elif self.type == 4002:
				player.addAmmo(4)
				return True

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

				if not alreadyChecked and (level[y][x] == 0 or level[y][x] > 999):
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
					if level[y][x] > 0 and level[y][x] <= 899:
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
					if level[y][x] > 0 and level[y][x] <= 899:
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
				if (room1.perimeterCoords[i] == room2.perimeterCoords[j] and ((level[room1.perimeterCoords[i][1]][room1.perimeterCoords[i][0]] == 0) or (level[room1.perimeterCoords[i][1]][room1.perimeterCoords[i][0]] > 899 and level[room1.perimeterCoords[i][1]][room1.perimeterCoords[i][0]] <= 999))):
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

				currentX, currentY = coord1[0], coord1[1]
				stepX, stepY = (coord2[0] - coord1[0]) / resolution, (coord2[1] - coord1[1]) / resolution
				for i in range(0,resolution):
					currentX += stepX
					currentY += stepY
					if (self.level[int(currentY)][int(currentX)] == 0 or self.level[int(currentY)][int(currentX)] >= 2000):
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

class NPCWeapon:
	def __init__(self, damage, range, bulletCount):
		self.damage = damage
		self.range = range
		self.bulletCount = bulletCount


	#Raycast check wall(simple, not a lot of checks)
	def checkWallDist(self, px, py, angle, level, doors):

		#Casting 1 ray to test functionality
		rayAng = angle

		#These booleans will run our while loops 
		horizCollision = False
		vertCollision = False

		#Keeps track of the distance from player to wall
		horizDist = 0.0
		vertDist = 0.0
		drawDist = 0.0

		#Resetting variables
		x = px
		y = py

		cX = 0
		cY = 0

		dX = 0
		dY = 0

		#Horizontal line checks
		#Is the player looking up or down? We have different distance to the next y integer point depending on the characters facing. Let's calculate those values.
		#Camera is looking up
		if rayAng >= math.pi:
			cY = int(py) - py
			dY = -1
			
		#Camera is looking down
		elif rayAng < math.pi:
			cY = int(py + 1) - py
			dY = 1

		#Calculate the change in x to the next integer from the starting position, as well as the change in x afterwards
		#If statement to verify that there will not be a divide by zero error
		if math.tan(rayAng) != 0:
			cX = cY / math.tan(rayAng)
			dX = dY / math.tan(rayAng)

		#Adjust (x,y) to the edge of the current tile the player is in, in the direction he is facing
		x += cX
		y += cY

		#Increment through steps, testing each horizontal line where y is an integer
		while (horizCollision == False):

			#Prevent out of bound error while looking through map array
			if int(y) >= len(level) or int(x) >= len(level[0]) or int(y) < 0 or int(x) < 0:
				horizDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
				horizCollision = True

			#Is the player looking up or down? This matters because the tile is seen as the top edge,
			#if we do not subtract 1 from y when looking up, it will look 1 block past where it should.
			#Player looking up
			elif rayAng >= math.pi:

				#Collision? If yes, break loop and have distance value set
				if (level[int(y-1)][int(x)] > 0 and level[int(y-1)][int(x)] <= 899):
					horizDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
					horizCollision = True

				#DOOR CHECK
				elif (level[int(y-1)][int(x)] > 899 and level[int(y-1)][int(x)] <= 999):
					
					currentTile = level[int(y-1)][int(x)]

					doorID = getDoor(doors, [int(x), int(y-1)])
		
					if int(y + 0.5*dY) < len(level) and int(y + 0.5*dY) >= 0 and int(x + 0.5*dX) < len(level) and int(x + 0.5*dX) >= 0:# and not doors[doorID].isOpen:				
						if (level[int(y - 1 - 0.5*dY)][int(x + 0.5*dX + doors[doorID].offset)] == currentTile):
							horizDist = math.sqrt(pow(x-px,2) + pow(y-py,2)) + 0.5
							horizCollision = True
						else:
							x += dX
							y += dY
					else:
						x += dX
						y += dY

				#Otherwise, keep incrementing
				else:	
					x += dX
					y += dY

			#Camera looking down
			elif rayAng < math.pi:

				#Collision? If yes, break loop and have distance value set
				if (level[int(y)][int(x)] > 0 and level[int(y)][int(x)] <= 899):
					horizDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
					horizCollision = True
				
				#DOOR CHECK
				elif (level[int(y)][int(x)] > 899 and level[int(y)][int(x)] <= 999):
					
					currentTile = level[int(y)][int(x)]

					doorID = getDoor(doors, [int(x), int(y)])
					
					if int(y + 0.5*dY) < len(level) and int(y + 0.5*dY) >= 0 and int(x + 0.5*dX) < len(level) and int(x + 0.5*dX) >= 0:# and not doors[doorID].isOpen:
						if (level[int(y + 0.5*dY)][int(x + 0.5*dX + doors[doorID].offset)] == currentTile):
							horizDist = math.sqrt(pow(x-px,2) + pow(y-py,2)) + 0.5
							horizCollision = True
						else:
							x += dX
							y += dY
					else:
						x += dX
						y += dY
				
				#Otherwise, keep incrementing
				else:	
					x += dX
					y += dY

		#Resetting variable values
		x = px
		y = py

		cX = 0
		cY = 0

		dX = 0
		dY = 0

		#Vertical line checks
		#Is the player looking right or left? We have different distance to the next x integer point depending on the characters facing. Let's calculate those values.
		#Camera is looking left
		if rayAng >= math.pi / 2 and rayAng <= math.pi * 3/2:
			cX = int(px) - px
			dX = -1

		#Camera is looking right
		elif rayAng > math.pi * 3/2 or rayAng < math.pi / 2: #Looking right
			cX = int(px + 1) - px
			dX = 1

		#Calculate the change in y to the next integer from the starting position, as well as the change in y afterwards
		cY = cX * math.tan(rayAng)
		dY = dX * math.tan(rayAng)

		#Adjust (x,y) to the edge of the current tile the player is in, in the direction he is facing
		x += cX 
		y += cY

		#Increment through steps, testing each vertical line where x is an integer
		while (vertCollision == False):

			#Prevent out of bound error while looking through map array
			if int(y) >= len(level) or int(x) >= len(level[0]) or int(y) < 0 or int(x) < 0:
				vertDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
				vertCollision = True

			#Is the player looking left or right? This matters because the tile is seen as the left edge,
			#if we do not subtract 1 from x when looking left, it will look 1 block past where it should.
			#Player looking left
			elif rayAng >= math.pi / 2 and rayAng <= math.pi * 3/2:
				#Collision? If yes, break loop and have distance value set
				if (level[int(y)][int(x-1)] > 0 and level[int(y)][int(x-1)] <= 899):
					vertDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
					vertCollision = True

				#DOOR CHECK
				elif (level[int(y)][int(x-1)] > 899 and level[int(y)][int(x-1)] <= 999):
					
					currentTile = level[int(y)][int(x-1)]

					doorID = getDoor(doors, [int(x), int(y)])
					
					if int(y + 0.5*dY) < len(level) and int(y + 0.5*dY) >= 0 and int(x + 0.5*dX) < len(level) and int(x + 0.5*dX) >= 0:# and not doors[doorID].isOpen:
						if (level[int(y + 0.5*dY + doors[doorID].offset)][int(x - 1 - 0.5*dX)] == currentTile):
							vertDist = math.sqrt(pow(x-px,2) + pow(y-py,2)) + 0.5
							vertCollision = True
						else:
							x += dX
							y += dY
					else:
						x += dX
						y += dY

				#Otherwise, continue incrementing
				else:	
					x += dX
					y += dY

			#Player looking right
			elif rayAng > math.pi * 3/2 or rayAng < math.pi / 2:	

				#Collision? If yes, break loop and have distance value set
				if (level[int(y)][int(x)] > 0 and level[int(y)][int(x)] <= 899):
					vertDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
					vertCollision = True
							
				#DOOR CHECK
				elif (level[int(y)][int(x)] > 899 and level[int(y)][int(x)] <= 999):
					
					currentTile = level[int(y)][int(x)]

					doorID = getDoor(doors, [int(x), int(y)])
					
					if int(y + 0.5*dY) < len(level) and int(y + 0.5*dY) >= 0 and int(x + 0.5*dX) < len(level) and int(x + 0.5*dX) >= 0:# and not doors[doorID].isOpen:
						if (level[int(y + 0.5*dY + doors[doorID].offset)][int(x + 0.5*dX)] == currentTile):
							vertDist = math.sqrt(pow(x-px,2) + pow(y-py,2)) + 0.5
							vertCollision = True
						else:
							x += dX
							y += dY
					else:
						x += dX
						y += dY

				#Otherwise, keep incrementing
				else:	
					x += dX
					y += dY

		#Most of the time, vertical distance and horizontal distance will be different.
		#We want to render using the shorter value, because it is the first intersection.
		if (vertDist >= horizDist):
			drawDist = horizDist
		elif (vertDist < horizDist):
			drawDist = vertDist

		#Return the distance from the 
		return drawDist

	def Shoot(self, enemy, player, level, doors):
		distToPlayer = math.sqrt(pow(player.x - enemy.x, 2) + pow(player.y - enemy.y, 2))
		distToWall = self.checkWallDist(player.x, player.y, math.atan((player.y - enemy.y) / (player.x - enemy.x)), level, doors)
		if distToPlayer < distToWall and distToPlayer <= self.range:
			Sound.Shoot_Sound(1)
			player.takeDamage(self.damage)