import math
class Camera:
	def __init__(self, coords, facing):

		#Define x, y, and angle through given coords and angle measure
		self.x, self.y = coords
		self.angle = facing

		self.health = 100

		#Define camera sensitivity & movement speed
		self.turnAdjust = math.pi / 64
		self.movementSpeed = 0.05
	def movePlayer(self, key, level):
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
		self.wallDetect(level)
	def wallDetect(self, level):
		xOffset = self.x - int(self.x)
		yOffSet = self.y - int(self.y)
		#Check to the front of the camera and adjust accordingly
		if (level[int(self.y + 0.2 * math.sin(self.angle))][int(self.x + 0.2 * math.cos(self.angle))] != 0):
			if (xOffset < self.movementSpeed or yOffSet < self.movementSpeed):
				self.x -= self.movementSpeed * math.cos(self.angle)
				self.y -= self.movementSpeed * math.sin(self.angle)
		#Check to the back of the camera and adjust accordingly
		if (level[int(self.y - 0.2 * math.sin(self.angle))][int(self.x - 0.2 * math.cos(self.angle))] != 0):
			if (xOffset < self.movementSpeed or yOffSet < self.movementSpeed):
				self.x += self.movementSpeed * math.cos(self.angle)
				self.y += self.movementSpeed * math.sin(self.angle)
		#Check to the left of the camera and adjust accordingly
		if (level[int(self.y - 0.2 * math.cos(self.angle))][int(self.x + 0.2 * math.sin(self.angle))] != 0):
			if (xOffset < self.movementSpeed or yOffSet < self.movementSpeed):
				self.x -= self.movementSpeed * math.sin(self.angle)
				self.y += self.movementSpeed * math.cos(self.angle)
		#Check to the right of the camera and adjust accordingly
		if (level[int(self.y + 0.2 * math.cos(self.angle))][int(self.x - 0.2 * math.sin(self.angle))] != 0):
			if (xOffset < self.movementSpeed or yOffSet < self.movementSpeed):
				self.x += self.movementSpeed * math.sin(self.angle)
				self.y -= self.movementSpeed * math.cos(self.angle)