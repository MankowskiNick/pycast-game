import pygame, sys, math
from pygame.locals import *

#Initialize Pygame
pygame.init()   

#Define colors
black = (0,0,0)
white = (255,255,255)
gray = (100,100,100)
red = (255,0,0)
blue = (0,0,255)

#Create dictionary of textures that can be easily referenced
spriteList = {
	#Wall Sprites
	1 : pygame.image.load("assets/wall.png"),
	2 : pygame.image.load("assets/window.png"),
	3 : pygame.image.load("assets/trunk.png"),

	#Object Sprites
	1000 : pygame.image.load("assets/barrel.png"),

	#NPC Sprites
	2000 : pygame.image.load("assets/enemy.png"),

	#Dead NPC Sprites
	#3000 : pygame.image.load("assets/dead.png")
}

#Define screen size
width = 800
height = 600
size = (width, height)

#Size Modifier, how large should the final image be rendered?
sizeModifier = height

#How many pixels should one ray render?
rayPixelWidth = 8

#How often should we shoot an npc ray? Every 10 pixels we can shoot one
npcSkip = 12

#How far should we look for NPCs?
npcRenderDist = 8

#Define camera field of view in radians
fov = 60 * math.pi / 180

#Create a clock used for controlling framerates
clock = pygame.time.Clock()

#Create font to render text on screen
font = pygame.font.Font(None, 30)

#Create screen object with global scope
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PyCasting")

#Blocksize to render minimap
blockSize = 10

#Textures are all squares, what are their dimensions?
spriteDimension = 16

#Bubble sort, used to sort the list of sprites to draw
def Sort(drawVect, sizeVect, coordVect):
	for i in range(0,len(sizeVect)):
		for k in range(0,len(sizeVect) - 1):
			if (sizeVect[k] > sizeVect[k+1]):
				sizeVect[k + 1], sizeVect[k] = sizeVect[k], sizeVect[k + 1]
				drawVect[k + 1], drawVect[k] = drawVect[k], drawVect[k + 1]
				coordVect[k + 1], coordVect[k] = coordVect[k], coordVect[k + 1]
	return drawVect, sizeVect, coordVect

#playerX, playerY, playerAngle, level as inputs
def drawOverlay(px, py, angle, npcList, drawMap):
	for x in range(0,len(drawMap[0])):
		for y in range(0,len(drawMap)):
			if (drawMap[y][x] > 0 and drawMap[y][x] <= 999):
				pygame.draw.rect(screen, black, pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize))
			elif  (drawMap[y][x] > 999):
				pygame.draw.circle(screen, black, (x * blockSize + blockSize / 2, y * blockSize + blockSize / 2), blockSize / 2)
			else:
				pygame.draw.rect(screen, white, pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize), 2)
	for i in range(0,len(npcList)):
		pygame.draw.circle(screen, blue,(npcList[i].x * blockSize, npcList[i].y * blockSize), 3)

	pygame.draw.circle(screen, black,(px * blockSize, py * blockSize), 3)
	pygame.draw.line(screen, black, (px * blockSize, py * blockSize), (px * blockSize + 8 * math.cos(angle), py * blockSize + 8 * math.sin(angle)))


	#Display FPS on Screen
	fps = font.render(str(int(clock.get_fps())) + " FPS (" + str(px) + " , " + str(py) + ")", True, white)
	screen.blit(fps, (0, height - 50))

def castRay(px, py, angle, currentLevel):
	#Define ray width
	rayWidth = fov / width

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
			if (currentLevel[int(y-1)][int(x)] > 0 and currentLevel[int(y-1)][int(x)] < 900):
				hx = x
				hy = y-1

				horizDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
				horizCollision = True

			#Otherwise, keep incrementing
			else:	
				x += dX
				y += dY

		#Camera looking down
		elif rayAng < math.pi:
			#Collision? If yes, break loop and have distance value set
			if (currentLevel[int(y)][int(x)] > 0 and currentLevel[int(y)][int(x)] < 900):
				hx = x
				hy = y

				horizDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
				horizCollision = True

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
			if (currentLevel[int(y)][int(x-1)] > 0 and currentLevel[int(y)][int(x-1)] < 900):
				vx = x-1
				vy = y

				vertDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
				vertCollision = True

			#Otherwise, continue incrementing
			else:	
				x += dX
				y += dY

		#Player looking right
		elif rayAng > math.pi * 3/2 or rayAng < math.pi / 2:
			#Collision? If yes, break loop and have distance value set
			if (currentLevel[int(y)][int(x)] > 0 and currentLevel[int(y)][int(x)] < 900):
				vx = x
				vy = y

				vertDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
				vertCollision = True

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
	pygame.draw.line(screen, red, (px * blockSize, py * blockSize), (blockSize * (px + drawDist*math.cos(rayAng)), blockSize * (py + drawDist*math.sin(rayAng))))

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

#Separate, less effecient, algorithm to raycast NPCs onto the screen, we can't just test @ integer steps
#for these dudes because they can have non integer coordinates
def castNPC(px, py, angle, npcList, currentLevel, shot):

	#Define step size
	step = 0.05

	#Starting from dist of 0
	npcDist = 0.0
	
	#Define starting coords
	x = px
	y = py

	#Create appropriately sized list of NPCs to render on screen
	renderList = []
	for i in range(0,len(npcList)):
		renderList.append([1,0])

	#Create container that allows us to ensure we only draw each NPC once
	hitCurrent = []
	for i in range(0,len(npcList)):
		hitCurrent.append(False)

	#We should only check the objects that are close to us
	checkList = []
	for i in range(0,len(npcList)):
		if (math.sqrt(pow(x - npcList[i].x, 2) + pow(y - npcList[i].y, 2)) <= npcRenderDist): 
			checkList.append(npcList[i])


	while (True):
		x += step * math.cos(angle)
		y += step * math.sin(angle)

		npcDist += step
		for i in range(0,len(checkList)):
			
			currentHitBox = checkList[i].hitBox

			minX = currentHitBox[0][0]
			maxX = currentHitBox[0][1]

			minY = currentHitBox[1][0]
			maxY = currentHitBox[1][1]

			if (x >= minX and x <= maxX and y >= minY and y <= maxY and hitCurrent[i] == False):

				#Indicate that the NPC can chase the player
				checkList[i].setActive()

				#Add npc to render list
				renderList[i] = [npcDist, checkList[i].type]
				hitCurrent[i] = True

			elif (hitCurrent):
				hitCurrent[i] = False

		if (npcDist > npcRenderDist):
			return renderList

#Render the scene given the player coords & level
def renderScene(px, py, pAng, currentLevel, npcList):

	#Define list containing currently rendered NPCs
	columnNPCList = []

	#Create columnNPCList deep enough to store data
	for i in range(0,width * len(npcList)):
		columnNPCList.append([[1,0], [1,0]])

	#Define default values for NPC rendering values
	npcSprite = spriteList[2000]
	npcDist = 1
	npcSize = 1
	npcSpriteID = 0

	#Draw background, ceiling and wall split in to two parts
	pygame.draw.rect(screen, gray, (0, 0, width, height / 2))
	pygame.draw.rect(screen, black, (0, height / 2, width, height / 2))

	#Cycle through eveny column of pixels on the screen and draw a column of the appropriate size for each

	drawList = []
	sizeList = []
	coordList = []
	for i in range(0,int(width / rayPixelWidth)):
		#Calculate current ray angle given fov and current camera angle
		currentAngle = ((pAng - fov/2) + (i * rayPixelWidth * fov / width))

		#Overflow for 2pi and 0
		if currentAngle > 2 * math.pi:
			currentAngle -= 2 * math.pi
		elif currentAngle < 0:
			currentAngle += 2 * math.pi

		#Define column length so that out draw function looks better
		enviroRenderOutput = castRay(px, py, currentAngle, currentLevel)

		#Disassemble output tuple
		columnLength, textureColumn = enviroRenderOutput

		#Draw column, each one will be centered vertically along screen.
		screen.blit(textureColumn, (i * rayPixelWidth, (height / 2) - (columnLength / 2)))

		#Render sprites and npcs

		#Only do this every several rays, defined by npcSkip
		if (int(i * rayPixelWidth / npcSkip) == i * rayPixelWidth / npcSkip):

			#Contain raycasting output into variable
			npcRenderOutput = castNPC(px, py, currentAngle, npcList, currentLevel, False)
			
			#How many NPCs are we drawing on the screen at once?
			npcRenderCount = len(npcRenderOutput)

			#Disassemble ouput from raycasting and reformat so we have info on the current
			#and most recently rendered column
			for k in range(0,npcRenderCount):

				#Disassemble array tuple
				npcDist = npcRenderOutput[k][0]
				npcSpriteID = npcRenderOutput[k][1]

				#Add sprite info to render list
				columnNPCList[k][0] = (columnNPCList[k][1])
				columnNPCList[k][1] = ([npcDist, npcSpriteID])

		#Draw sprites & NPCs, don't allow out of bounds exception
		#Don't allow out of bounds exception
		if (i != 0):
			#Go backwards so that we are drawing the farthest NPC first
			for k in range(npcRenderCount, -1, -1):

				#Check and see if column is last column of the current NPC being drawn
				if (columnNPCList[k][1][1] == 0 and columnNPCList[k][0][1] != 0):

					#If yes, Declare sprite size
					npcSize = int(sizeModifier / columnNPCList[k][0][0])
					
					#Define texture given NPC ID
					npcSprite = spriteList[columnNPCList[k][0][1]]

					#Scale sprite to defined size
					#npcSprite = pygame.transform.scale(npcSprite, (npcSize, npcSize))

					#Only render NPC if it should be closer than the wall
					if (npcSize > columnLength):

						#Render NPC
						#screen.blit(npcSprite, ((i * rayPixelWidth) - npcSize, (height / 2) - (npcSize / 2)))
						drawList.append(pygame.transform.scale(npcSprite, (npcSize, npcSize)))
						sizeList.append(npcSize)
						coordList.append(((i * rayPixelWidth) - npcSize, (height / 2) - (npcSize / 2)))

	drawList, sizeList, coordList = Sort(drawList, sizeList, coordList)

	for k in range(0,len(sizeList)):
		screen.blit(drawList[k], (coordList[k]))