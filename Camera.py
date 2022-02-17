import math

def getDoor(doors, coords):
	for i in range(0, len(doors)):
		if math.sqrt(pow(doors[i].x + 0.5 - coords[0], 2) + pow(doors[i].y + 0.5 - coords[1], 2)) < 0.8:
			return i
	return 0

class Camera:
	def __init__(self, coords, facing):

		#Define x, y, and angle through given coords and angle measure
		self.x, self.y = coords
		self.angle = facing

		self.hp = 100

		self.ammoCount = [
			32,
			12,
		]

		#Define camera sensitivity & movement speed
		self.turnAdjust = math.pi / 64
		self.movementSpeed = 0.05
	def movePlayer(self, key, level, doors):
		#Check to ensure that degree is not overshot past 2pi or 0
		if self.angle > math.pi * 2:
			self.angle = 0 + self.turnAdjust
		elif self.angle < 0:
			self.angle = math.pi * 2 - self.turnAdjust

		#W key, fordward
		if key == 119:
			self.x += self.movementSpeed*math.cos(self.angle)
			self.y += self.movementSpeed*math.sin(self.angle)
		#S key, backward
		if key == 115:
			self.x -= self.movementSpeed*math.cos(self.angle)
			self.y -= self.movementSpeed*math.sin(self.angle)
		#A key, left
		if key == 97:
			self.x += self.movementSpeed*math.sin(self.angle)
			self.y -= self.movementSpeed*math.cos(self.angle)
		#D key, right
		if key == 100:
			self.x -= self.movementSpeed*math.sin(self.angle)
			self.y += self.movementSpeed*math.cos(self.angle)
		#J key, turn left
		if key == 106:
			self.angle -= self.turnAdjust
		#L key, turn right
		if key == 108:
			self.angle += self.turnAdjust
		self.wallDetect(level, doors)
	def wallDetect(self, level, doors):
		xOffset = self.x - int(self.x)
		yOffSet = self.y - int(self.y)

		#Check to the front of the camera and adjust accordingly
		currentTile = level[int(self.y + 0.2 * math.sin(self.angle))][int(self.x + 0.2 * math.cos(self.angle))]
		doorID = getDoor(doors, [self.x + 0.2 * math.cos(self.angle), self.y + 0.2 * math.sin(self.angle)])
		if (currentTile > 0 and currentTile <= 899) or (currentTile > 999 and currentTile <= 1999) or (currentTile > 899 and currentTile <= 999 and (not doors[doorID].isOpen) and (not doorID == 0)):
			if (xOffset < self.movementSpeed or yOffSet < self.movementSpeed):
				self.x -= self.movementSpeed * math.cos(self.angle)
				self.y -= self.movementSpeed * math.sin(self.angle)
		#Check to the back of the camera and adjust accordingly
		currentTile = level[int(self.y - 0.2 * math.sin(self.angle))][int(self.x - 0.2 * math.cos(self.angle))]
		doorID = getDoor(doors, [self.x - 0.2 * math.cos(self.angle), self.y - 0.2 * math.sin(self.angle)])
		if (currentTile > 0 and currentTile <= 899) or (currentTile > 999 and currentTile <= 1999) or (currentTile > 899 and currentTile <= 999 and (not doors[doorID].isOpen) and (not doorID == 0)):
			if (xOffset < self.movementSpeed or yOffSet < self.movementSpeed):
				self.x += self.movementSpeed * math.cos(self.angle)
				self.y += self.movementSpeed * math.sin(self.angle)
		#Check to the left of the camera and adjust accordingly
		doorID = getDoor(doors, [self.x + 0.2 * math.sin(self.angle), self.y - 0.2 * math.cos(self.angle)])
		currentTile = level[int(self.y - 0.2 * math.cos(self.angle))][int(self.x + 0.2 * math.sin(self.angle))]
		if (currentTile > 0 and currentTile <= 899) or (currentTile > 999 and currentTile <= 1999) or (currentTile > 899 and currentTile <= 999 and (not doors[doorID].isOpen) and (not doorID == 0)):
			if (xOffset < self.movementSpeed or yOffSet < self.movementSpeed):
				self.x -= self.movementSpeed * math.sin(self.angle)
				self.y += self.movementSpeed * math.cos(self.angle)
		#Check to the right of the camera and adjust accordingly
		doorID = getDoor(doors, [self.x - 0.2 * math.sin(self.angle), self.y + 0.2 * math.cos(self.angle)])
		currentTile = level[int(self.y + 0.2 * math.cos(self.angle))][int(self.x - 0.2 * math.sin(self.angle))]
		if (currentTile > 0 and currentTile <= 899) or (currentTile > 999 and currentTile <= 1999) or (currentTile > 899 and currentTile <= 999 and (not doors[doorID].isOpen) and (not doorID == 0)):
			if (xOffset < self.movementSpeed or yOffSet < self.movementSpeed):
				self.x += self.movementSpeed * math.sin(self.angle)
				self.y -= self.movementSpeed * math.cos(self.angle)
	
	def addHealth(self, hp):
		self.hp += hp

		if self.hp > 100:
			self.hp == 100
	
	def addAmmo(self, count):
		for i in range(0,len(self.ammoCount)):
			self.ammoCount[i] += count