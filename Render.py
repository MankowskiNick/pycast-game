import pygame, sys, math, configparser
from pygame.locals import *
from Sprites import *

#Initialize Pygame
pygame.init()   

#Define colors
black = (0,0,0)
white = (255,255,255)
gray = (100,100,100)
red = (255,0,0)
blue = (0,0,255)
brown = (235, 143, 52)

#Create config parser to read in data from config files
gfxConfig = configparser.ConfigParser()

#Read data values from config file
gfxConfig.read('gfx.conf')
width = int(gfxConfig['WINDOW']['width'])
height = int(gfxConfig['WINDOW']['height'])
fullscreen = gfxConfig.getboolean('WINDOW', 'fullscreen')
rayPixelWidth = int(gfxConfig['RENDER']['RayResolution'])
spriteDimension = int(gfxConfig['RENDER']['SpriteDimension'])
fov = int(gfxConfig['RENDER']['FOV']) * math.pi / 180
blockSize = int(gfxConfig['MINIMAP']['MinimapBlockSize'])
drawMinimap = gfxConfig.getboolean('MINIMAP', 'DrawMiniMap')

#Scalar used to draw heights at the appropriate height
sizeModifier = height * 3 / 4

#Create a clock used for controlling framerates
clock = pygame.time.Clock()

#Create font to render text on screen
font = pygame.font.Font(None, 30)

#Create screen object with global scope
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PyCasting")

#Load UI
UI = pygame.image.load("assets/system/gui.png")
UI_scaleX, UI_scaleY = width / UI.get_width(), height / UI.get_height()
UI = pygame.transform.scale(UI, (width, height))

minimapSprites = createSpriteList()
for key in minimapSprites.keys():
	minimapSprites[key] = pygame.transform.scale(minimapSprites[key], (blockSize, blockSize))


#Toggle fullscreen if desired
if fullscreen: pygame.display.toggle_fullscreen()


#Convert int to list representing 3 digits
def intToList(n):
	if n > 999:
		return [9, 9, 9]
	else:
		dig1 = int(n / 100)
		dig2 = int(n / 10) - (dig1 * 10)
		dig3 = int(n) - (dig1 * 100) - (dig2 * 10)
		return [dig1, dig2, dig3]


#Bubble sort, used to sort the list of sprites to draw
def Sort(vect):
	for i in range(0,len(vect)):
		for k in range(0,len(vect) - 1):
			if (vect[k][1] > vect[k+1][1]):
				vect[k], vect[k+1] = vect[k+1], vect[k]
	return vect

def drawOverlay(player, screen, npcList, drawMap):
	px, py, angle = player.x, player.y, player.angle
	if drawMinimap:	
		pygame.draw.rect(screen, white, pygame.Rect(0, 0, len(drawMap[0]) * blockSize, len(drawMap) * blockSize))
		for x in range(0,len(drawMap[0])):
			for y in range(0,len(drawMap)):
				if (drawMap[y][x] > 0 and drawMap[y][x] <= 999):
					screen.blit(minimapSprites[drawMap[y][x]], (x * blockSize, y * blockSize))
		for i in range(0,len(npcList)):
			screen.blit(pygame.transform.scale(npcList[i].currentSprite, (blockSize, blockSize)), ((npcList[i].x - 0.5) * blockSize, (npcList[i].y - 0.5) * blockSize))

		pygame.draw.circle(screen, black,(px * blockSize, py * blockSize), 3)
		pygame.draw.line(screen, black, (px * blockSize, py * blockSize), (px * blockSize + 8 * math.cos(angle), py * blockSize + 8 * math.sin(angle)))


	#Display FPS on Screen
	fps = font.render(str(int(clock.get_fps())) + " FPS (" + str(px) + " , " + str(py) + ") : " + str(player.angle), True, white)
	#fps = font.render(str(int(clock.get_fps())) + "  (" + str(px) + " , " + str(py) + ")", True, white)

	screen.blit(fps, (0, height - 150))

def getDoor(doors, coords):
	for i in range(0, len(doors)):
		if math.sqrt(pow(doors[i].x + 0.5 - coords[0], 2) + pow(doors[i].y + 0.5 - coords[1], 2)) <= 1:
			return i
	return 0

def castRay(px, py, angle, currentLevel, spriteList, doors):

	#Casting 1 ray to test functionality
	rayAng = angle

	#Temporary container for x & y of the current collision point
	tx = 0
	ty = 0

	#These booleans will run our while loops 
	horizCollision = False
	vertCollision = False

	#Keeps track of the distance from player to wall
	horizDist = 1.0
	vertDist = 1.0
	drawDist = 1.0

	#Reset pixel offset
	pixelOffset = 0

	#Reset wall texture
	wallTexture = spriteList[1]

	#Resetting variables
	x = px
	y = py

	hx = x
	hy = y

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
	if math.tan(rayAng != 0):
		cX = cY / math.tan(rayAng)
		dX = dY / math.tan(rayAng)

	#Adjust (x,y) to the edge of the current tile the player is in, in the direction he is facing
	x += cX
	y += cY

	#Increment through steps, testing each horizontal line where y is an integer
	while (horizCollision == False):

		#Prevent out of bound error while looking through map array
		if int(y) >= len(currentLevel) or int(x) >= len(currentLevel[0]) or int(y) < 0 or int(x) < 0:
			hx = x
			hy = y

			horizDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
			horizCollision = True

		#Is the player looking up or down? This matters because the tile is seen as the top edge,
		#if we do not subtract 1 from y when looking up, it will look 1 block past where it should.
		#Player looking up
		elif rayAng >= math.pi:
			#Collision? If yes, break loop and have distance value set
			if (currentLevel[int(y-1)][int(x)] > 0 and currentLevel[int(y-1)][int(x)] <= 899):
				hx = x
				hy = y-1

				horizDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
				horizCollision = True
			
			#DOOR CHECK
			elif (currentLevel[int(y-1)][int(x)] > 899 and currentLevel[int(y-1)][int(x)] <= 999):
				
				currentTile = currentLevel[int(y-1)][int(x)]

				doorID = getDoor(doors, [int(x), int(y-1)])
	
				if int(y + 0.5*dY) < len(currentLevel) and int(y + 0.5*dY) >= 0 and int(x + 0.5*dX) < len(currentLevel) and int(x + 0.5*dX) >= 0:# and not doors[doorID].isOpen:				
					if (currentLevel[int(y - 1 - 0.5*dY)][int(x + 0.5*dX + doors[doorID].offset)] == currentTile):
						hx = x + 0.5*dX + doors[doorID].offset
						hy = y - 1 - 0.5*dY
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
			if (currentLevel[int(y)][int(x)] > 0 and currentLevel[int(y)][int(x)] <= 899):
				hx = x
				hy = y

				horizDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
				horizCollision = True

			#DOOR CHECK
			elif (currentLevel[int(y)][int(x)] > 899 and currentLevel[int(y)][int(x)] <= 999):
				
				currentTile = currentLevel[int(y)][int(x)]

				doorID = getDoor(doors, [int(x), int(y)])
				
				if int(y + 0.5*dY) < len(currentLevel) and int(y + 0.5*dY) >= 0 and int(x + 0.5*dX) < len(currentLevel) and int(x + 0.5*dX) >= 0:# and not doors[doorID].isOpen:
					if (currentLevel[int(y + 0.5*dY)][int(x + 0.5*dX + doors[doorID].offset)] == currentTile):
						hx = x + 0.5*dX + doors[doorID].offset
						hy = y + 0.5*dY
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

	vx = x
	vy = y

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
		if int(y) >= len(currentLevel) or int(x) >= len(currentLevel[0]) or int(y) < 0 or int(x) < 0:
			vx = x
			vy = y

			vertDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
			vertCollision = True

		#Is the player looking left or right? This matters because the tile is seen as the left edge,
		#if we do not subtract 1 from x when looking left, it will look 1 block past where it should.
		#Player looking left
		elif rayAng >= math.pi / 2 and rayAng <= math.pi * 3/2:
			#Collision? If yes, break loop and have distance value set
			if (currentLevel[int(y)][int(x-1)] > 0 and currentLevel[int(y)][int(x-1)] <= 899):
				vx = x-1
				vy = y

				vertDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
				vertCollision = True
			
			#DOOR CHECK
			elif (currentLevel[int(y)][int(x-1)] > 899 and currentLevel[int(y)][int(x-1)] <= 999):
				
				currentTile = currentLevel[int(y)][int(x-1)]

				doorID = getDoor(doors, [int(x), int(y)])
				
				if int(y + 0.5*dY) < len(currentLevel) and int(y + 0.5*dY) >= 0 and int(x + 0.5*dX) < len(currentLevel) and int(x + 0.5*dX) >= 0:# and not doors[doorID].isOpen:
					if (currentLevel[int(y + 0.5*dY + doors[doorID].offset)][int(x - 1 - 0.5*dX)] == currentTile):
						vx = x - 1 - 0.5*dX
						vy = y + 0.5*dY + doors[doorID].offset
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
			if (currentLevel[int(y)][int(x)] > 0 and currentLevel[int(y)][int(x)] <= 899):
				vx = x
				vy = y

				vertDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
				vertCollision = True
						
			#DOOR CHECK
			elif (currentLevel[int(y)][int(x)] > 899 and currentLevel[int(y)][int(x)] <= 999):
				
				currentTile = currentLevel[int(y)][int(x)]

				doorID = getDoor(doors, [int(x), int(y)])
				
				if int(y + 0.5*dY) < len(currentLevel) and int(y + 0.5*dY) >= 0 and int(x + 0.5*dX) < len(currentLevel) and int(x + 0.5*dX) >= 0:# and not doors[doorID].isOpen:
					if (currentLevel[int(y + 0.5*dY + doors[doorID].offset)][int(x + 0.5*dX)] == currentTile):
						vx = x + 0.5*dX
						vy = y + 0.5*dY + doors[doorID].offset
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

		#Update coords of collision
		tx = hx
		ty = hy

		#Calculate pixel offset for image, what row of pixels will we have to render?
		pixelOffset = int(spriteDimension * (tx - int(tx)))
	elif (vertDist < horizDist):
		drawDist = vertDist

		#Update coords of collision
		tx = vx
		ty = vy

		#Calculate pixel offset for image, what column of pixels will we have to render?
		pixelOffset = (spriteDimension * (ty - int(ty)))

	#Draws the FOV of the player in red
	#pygame.draw.line(screen, red, (px * blockSize, py * blockSize), (blockSize * (px + drawDist*math.cos(rayAng)), blockSize * (py + drawDist*math.sin(rayAng))))

	#Define what sprite will be our reference to render
	if (currentLevel[int(ty)][int(tx)] > 0):
		wallTexture = spriteList[currentLevel[int(ty)][int(tx)]].subsurface((pixelOffset, 0, 1, spriteDimension))

	#Resize sprite to fit height needed
	wallTexture = pygame.transform.scale(wallTexture, (rayPixelWidth, int(sizeModifier / drawDist)))

	#Return what value the height of the column should be and the formatted sprite
	if drawDist != 0:
		return sizeModifier / drawDist, wallTexture
	else:
		return 0, wallTexture

#Raycast check wall(simple, not a lot of checks)
def checkWallDist(px, py, angle, level, doors):

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

def drawObj(screen, x, y, angle, npcList, spriteList, level, doors):
	#Create empty list of objects to draw
	drawVect = []
	
	#Cycle through every object
	for i in range(0,len(npcList)):
		#Determine object angle from origin line at camera position
		objAngleFromOrig = math.atan((npcList[i].y - y) / (npcList[i].x - x))
		if npcList[i].x - x < 0:
			objAngleFromOrig += math.pi

		#Calculate difference between object angle and camera facing
		angleDiff = objAngleFromOrig - angle
		
		#Adjust values accordingly to fall within trig parameters
		while objAngleFromOrig > math.pi * 2:
			objAngleFromOrig -= math.pi * 2
		while objAngleFromOrig < 0:
			objAngleFromOrig += math.pi * 2

		while angleDiff < 0:
			angleDiff += math.pi * 2
		while angleDiff > math.pi:
			angleDiff -= math.pi * 2

		#If the difference in angle falls within the FOV
		if abs(angleDiff) <= fov / 1.5:
			
			#Calculate obj dist and the distance to the nearest wall
			distToObj = math.sqrt(pow(npcList[i].x - x, 2) + pow(npcList[i].y - y, 2))
			distToWall = checkWallDist(x, y, objAngleFromOrig, level, doors)

			#If the object is closer than the nearest wall, add to draw vector
			if distToWall > distToObj:
				drawVect.append([npcList[i], distToObj, angleDiff])
				npcList[i].setActive()

	#Sort things by how close they are
	Sort(drawVect)

	#Render them in order from furthest to closest, closest being draw on top
	for i in range(len(drawVect) - 1, -1, -1):
		drawSize = sizeModifier / drawVect[i][1]
		sprite = drawVect[i][0].currentSprite
		if drawSize < width * 2:
			sprite = pygame.transform.scale(sprite, (drawSize, drawSize))
			xDisp = drawVect[i][1] * math.sin(drawVect[i][2])
			xRange = 2 * drawVect[i][1] * math.sin(fov / 2)
			xPos = ((xDisp / xRange) * width) + (width / 2)
			screen.blit(sprite, (xPos - sprite.get_width() / 2, (height / 2) - (sprite.get_height() / 2) ))

#Render the scene given the player coords & level
def renderScene(player, currentLevel, npcList, spriteList, currentWeapon, frameCount, font, doors):
	
	#Draw background, ceiling and wall split in to two parts
	pygame.draw.rect(screen, black, (0, 0, width, height / 2))
	pygame.draw.rect(screen, gray, (0, height / 2, width, height / 2))

	#Cycle through eveny column of pixels on the screen and draw a column of the appropriate size for each
	for i in range(0,int(width / rayPixelWidth)):
		#Calculate current ray angle given fov and current camera angle
		currentAngle = ((player.angle - fov/2) + (i * rayPixelWidth * fov / width))

		#Overflow for 2pi and 0
		if currentAngle > 2 * math.pi:
			currentAngle -= 2 * math.pi
		elif currentAngle < 0:
			currentAngle += 2 * math.pi

		#Define column length so that out draw function looks better
		enviroRenderOutput = castRay(player.x, player.y, currentAngle, currentLevel, spriteList, doors)

		#Disassemble output tuple
		columnLength, textureColumn = enviroRenderOutput

		#Draw column, each one will be centered vertically along screen.
		screen.blit(textureColumn, (i * rayPixelWidth, (height / 2) - (columnLength / 2)))

	#Render sprites and npcs
	drawObj(screen, player.x, player.y, player.angle, npcList, spriteList, currentLevel, doors)

	#Render smoke cloud from barrel
	if frameCount - currentWeapon.shotFrame <= 2 and frameCount - currentWeapon.shotFrame >= 0 and currentWeapon.id != 0:
		screen.blit(currentWeapon.boomList[frameCount - currentWeapon.shotFrame], (0, 60 + currentWeapon.yOffset))
	
	#Render Weapon
	screen.blit(currentWeapon.currentSprite, (0,60 + currentWeapon.yOffset))
	
	#Draw UI
	screen.blit(UI, (0,0))
	
	#Draw ammo count & health
	if player.ammoCount[currentWeapon.ammoID] <= 999 and player.ammoCount[currentWeapon.ammoID] >= 0:
		ammoCountList = intToList(player.ammoCount[currentWeapon.ammoID])
	else:
		ammoCountList = [9,9,9]
	if player.hp <= 100 and player.hp >= 0:
		healthCountList = intToList(player.hp)
	else:
		healthCountList = [0,0,0]
	
	screen.blit(font[healthCountList[0]], (1 * UI_scaleX, height - (4 * UI_scaleY)))
	screen.blit(font[healthCountList[1]], (3 * UI_scaleX, height - (4 * UI_scaleY)))
	screen.blit(font[healthCountList[2]], (5 * UI_scaleX, height - (4 * UI_scaleY)))

	screen.blit(font[ammoCountList[0]], (width - (7 * UI_scaleX), height - (4 * UI_scaleY)))
	screen.blit(font[ammoCountList[1]], (width - (5 * UI_scaleX), height - (4 * UI_scaleY)))
	screen.blit(font[ammoCountList[2]], (width - (3 * UI_scaleX), height - (4 * UI_scaleY)))

	#Draw minimap
	drawOverlay(player, screen, npcList, currentLevel)