import math

#Find NPCs and create database of them along with coords
def findNPC(focusMap):                                         
	npcList = []
	for x in range(0,len(focusMap[0])):
		for y in range(0,len(focusMap)):
			if focusMap[y][x] > 999 and focusMap[y][x] < 2000:
				npcList.append(NPC((x, y), focusMap[y][x], len(npcList)))
				#focusMap[y][x] = 0
			if focusMap[y][x] > 1999:# and focusMap[y][x]:
				npcList.append(NPC((x, y), focusMap[y][x], len(npcList)))
				focusMap[y][x] = 0
			else:
				continue
	return npcList

class NPC:
	def __init__(self, coords, type, label):
		#Define coords
		self.x, self.y = coords

		self.startX, self.startY = coords

		#Adjust coords
		self.x += 0.5
		self.y += 0.5

		#Define type
		self.type = type

		#Define if NPC is static object or actual npc
		if (self.type < 2000):
			self.isObject = True
		else:
			self.isObject = False

		#Define label, position in the npcList array that this npc lies
		self.label = label

		#Define step size
		self.stepSize = 0.01

		#Define whether or not to display dead person sprite
		self.isAlive = True

		self.xDisp = 0
		self.yDisp = 0

		#Define npc as not active, npc hasnt been seen
		self.deActivate()

		#stored as [[x0,x1],[y0,y1]]
		self.updateHitBox()

	def walk(self, pCoords, level, npcList):
		if (self.isActive and not self.isObject):
			px, py = pCoords

			xDist = px - self.x
			yDist = py - self.y
			distTo = math.sqrt(pow(xDist, 2) + pow(yDist, 2))

			self.xDisp = self.stepSize * xDist / distTo
			self.yDisp = self.stepSize * yDist / distTo

			if (self.wallDetect(level) == False and self.npcDetect(npcList) == False and distTo > 1):
				self.x += self.xDisp
				self.y += self.yDisp

		self.updateHitBox()

	def wallDetect(self, level):
		if (level[int(self.y + self.yDisp)][int(self.x + self.xDisp)] > 0):
			return True
		else:
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
					checkX = self.x + 0.5 * math.cos(currentAngle)
					checkY = self.y + 0.5 * math.sin(currentAngle)
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
		self.hitBox = [[self.x - 0.25, self.x + 0.25],[self.y - 0.25, self.y + 0.25]]
	
	def updateLabel(self, n):
		self.label = n