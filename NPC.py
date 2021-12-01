import math

#Find NPCs and create database of them along with coords
def findNPC(focusMap):                                         
	npcList = []
	for x in range(0,len(focusMap[0])):
		for y in range(0,len(focusMap)):
			if focusMap[y][x] > 999:
				npcList.append(NPC((x, y), focusMap[y][x], len(npcList)))
				focusMap[y][x] = 0
			else:
				continue
	return npcList

class NPC:
	def __init__(self, coords, type, label):
		#Define coords
		self.x, self.y = coords

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


			xDisplacement = self.stepSize * xDist / distTo
			yDisplacement = self.stepSize * yDist / distTo

			if (self.wallDetect((xDisplacement, yDisplacement), level, npcList) == False and distTo > 1):
				self.x += xDisplacement
				self.y += yDisplacement

		self.updateHitBox()

	def wallDetect(self, displacement, level, npcList):
		xDisplacement, yDisplacement = displacement

		for i in range(0,len(npcList)):
			if (i != self.label):
				if (math.sqrt(pow(self.x - npcList[i].x, 2) + pow(self.y - npcList[i].y, 2)) < 1 and self.isAlive):
					if (self.x >= npcList[i].x):
						self.x += self.stepSize
					else:
						self.x -= self.stepSize
					if (self.y >= npcList[i].y):
						self.y += self.stepSize
					else:
						self.y -= self.stepSize
					return True
				else:
					continue

		if (level[int(self.y + yDisplacement)][int(self.x + xDisplacement)] > 0):
			return True
		else:
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