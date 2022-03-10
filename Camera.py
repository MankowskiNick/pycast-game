import math, Sound

#Get the door nearest to the player
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

		#Define health and that the player is alive
		self.hp = 85
		self.isAlive = True

		#Define ammo counts
		self.ammoCount = [
			32,
			12,
			99999999999999999,
		]

		#Define camera sensitivity & movement speed
		self.turnAdjust = math.pi / 64
		self.movementSpeed = 0.05

	def movePlayer(self, key, level, doors, npcList):

		#If the player is alive, allow movement
		if self.isAlive:

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

			#Check for collisions
			self.wallDetect(level, doors)
			self.npcDetect(npcList)

	def wallDetect(self, level, doors):

		#Check how far we are from the rounded down integer value tile
		xOffset = self.x - int(self.x)
		yOffSet = self.y - int(self.y)

		#Check to the front of the camera and adjust accordingly
		currentTile = level[int(self.y + 0.2 * math.sin(self.angle))][int(self.x + 0.2 * math.cos(self.angle))]
		
		#Find if there is a door nearby
		doorID = getDoor(doors, [self.x + 0.2 * math.cos(self.angle), self.y + 0.2 * math.sin(self.angle)])
		
		#Check to see if we can mititage the collision
		if (currentTile > 0 and currentTile <= 899) or (currentTile > 999 and currentTile <= 1999) or (currentTile > 899 and currentTile <= 999 and (not doors[doorID].isOpen) and (not doorID == 0)):
			if (xOffset < self.movementSpeed or yOffSet < self.movementSpeed):
				self.x -= self.movementSpeed * math.cos(self.angle)
				self.y -= self.movementSpeed * math.sin(self.angle)
		
		#Check to the back of the camera and adjust accordingly
		currentTile = level[int(self.y - 0.2 * math.sin(self.angle))][int(self.x - 0.2 * math.cos(self.angle))]
		
		#Find if there is a door nearby
		doorID = getDoor(doors, [self.x - 0.2 * math.cos(self.angle), self.y - 0.2 * math.sin(self.angle)])
		
		#Check to see if we can mititage the collision
		if (currentTile > 0 and currentTile <= 899) or (currentTile > 999 and currentTile <= 1999) or (currentTile > 899 and currentTile <= 999 and (not doors[doorID].isOpen) and (not doorID == 0)):
			if (xOffset < self.movementSpeed or yOffSet < self.movementSpeed):
				self.x += self.movementSpeed * math.cos(self.angle)
				self.y += self.movementSpeed * math.sin(self.angle)

		#Check to the left of the camera and adjust accordingly
		currentTile = level[int(self.y - 0.2 * math.cos(self.angle))][int(self.x + 0.2 * math.sin(self.angle))]
	
		#Find if there is a door nearby
		doorID = getDoor(doors, [self.x + 0.2 * math.sin(self.angle), self.y - 0.2 * math.cos(self.angle)])

		#Check to see if we can mititage the collision
		if (currentTile > 0 and currentTile <= 899) or (currentTile > 999 and currentTile <= 1999) or (currentTile > 899 and currentTile <= 999 and (not doors[doorID].isOpen) and (not doorID == 0)):
			if (xOffset < self.movementSpeed or yOffSet < self.movementSpeed):
				self.x -= self.movementSpeed * math.sin(self.angle)
				self.y += self.movementSpeed * math.cos(self.angle)

		#Check to the right of the camera and adjust accordingly
		currentTile = level[int(self.y + 0.2 * math.cos(self.angle))][int(self.x - 0.2 * math.sin(self.angle))]
		
		#Find if there is a door nearby		
		doorID = getDoor(doors, [self.x - 0.2 * math.sin(self.angle), self.y + 0.2 * math.cos(self.angle)])
		
		#Check to see if we can mititage the collision
		if (currentTile > 0 and currentTile <= 899) or (currentTile > 999 and currentTile <= 1999) or (currentTile > 899 and currentTile <= 999 and (not doors[doorID].isOpen) and (not doorID == 0)):
			if (xOffset < self.movementSpeed or yOffSet < self.movementSpeed):
				self.x += self.movementSpeed * math.sin(self.angle)
				self.y -= self.movementSpeed * math.cos(self.angle)
	
	def npcDetect(self, npcList):
		for npc in npcList:
			if (npc.distToPlayer < 0.3 and npc.distToPlayer > 0):
				angleToNPC = math.tan((npc.y - self.y) / (npc.x - self.x))
				xScale = (npc.x - self.x) / npc.distToPlayer
				yScale = (npc.y - self.y) / npc.distToPlayer

				self.x -= xScale * 0.2
				self.y -= yScale * 0.2

	#This will be called by a pickup being activated
	def addHealth(self, hp):

		#Add health
		self.hp += hp

		#Check if adding this health will overflow the health, 
		#if it will contribute some or all of the hp return true to eliminate the pickup.
		#If the health is full, don't add to the current HP and return False to inform that 
		#the pickup shouldn't be removed
		if self.hp == 100 + hp:
			self.hp -= hp
			return False
		elif self.hp > 100:
			self.hp = 100
			return True
		else:
			return True
	
	def addAmmo(self, count):
		for i in range(0,len(self.ammoCount)):
			self.ammoCount[i] += count
	
	def takeDamage(self, damage):
		self.hp -= damage
		if self.hp <= 0:
			self.isAlive = False

	def updateWeapon(self, weapon):
		self.weapon = weapon