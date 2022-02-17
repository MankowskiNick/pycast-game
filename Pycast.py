#Import necessary Python libraries
import pygame, sys, math
from pygame.locals import *

#Import custom libraaries
import Render, Format, Camera, NPC, LevelCreator, Sprites, Weapon, Door
from Global import *
from Render import *
#from Format import *
from Sprites import *
from Weapon import *

#Initialize pygame
pygame.init()

#Load map and NPC list
mapLevel, npcList, tmp1, tmp2, tmp3 = LevelCreator.loadMapFromFile("levels/level.leveldata")
del tmp1, tmp2, tmp3

#Load in doors
doors = Door.findDoors(mapLevel)

#Create player olbject with coords found by findPlayer
player = Camera.Camera(Format.findPlayer(mapLevel), 0)

#Create a HIRs of the level
levelHIR= NPC.HIRs(mapLevel)
for i in range(0,len(npcList)):
	npcList[i].giveHIR(levelHIR, player, mapLevel)

#Create all sprite lists used by program
spriteList = createSpriteList()
boomList = createBoomList(width, height)
weaponSpriteList = createWeapSpriteList(width, height)

#Create font used to render numbers
font = createFont(width, height)

#Create weapon list
weaponList = [
	Weapon(1, 25, 8, 4, 0, weaponSpriteList[1], boomList),
	Weapon(1, 50, 3.5, 20, 1, weaponSpriteList[2], boomList),
]

#Declare values needed 
currentWeapon = weaponList[0]

frameCount = 0

#Define sensitivity
sensitivity = 0.8

#Set cursor to invisible
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

while True:
	frameCount+=1

	#Set framerate
	clock.tick(60)
	pygame.key.set_repeat(10,10)

	#Update NPCs
	for i in range(0,len(npcList)):
		if npcList[i].walk(player, mapLevel, npcList, doors, frameCount):

			#cull the npc if it true
			npcList.pop(i)
			break
	
	for n in range(0, len(npcList)):
		npcList[n].updateLabel(n)

	for door in doors:
		door.update()

	#Cycle through each event that occurs in a frame
	for event in pygame.event.get():

		#Make sure we can exit the window
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		#Handling keyboard input
		elif event.type == KEYDOWN:

			#Handling escape key exitcle
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()
			if len(weaponList) <= 9 and len(weaponList) > 0:
				for i in range(0, len(weaponList)):
					if event.key == i + 49:
						currentWeapon = weaponList[i]

			#Move player according to key
			player.movePlayer(event.key, mapLevel, doors)
			if event.key == pygame.K_m:
				mapLevel, npcList = LevelCreator.Main(player.x, player.y, mapLevel, npcList)

			elif event.key == pygame.K_SPACE:
				Door.openDoor(doors, [player.x, player.y], frameCount)

		#Move mouse and adjust camera angle accordingly
		elif event.type == MOUSEMOTION:
			player.angle -= (width / 2 - pygame.mouse.get_pos()[0]) / (width * (1 / sensitivity))

			pygame.mouse.set_pos(width / 2, height / 2)
		
		#Get state of mousebutton to determine whether to shoot or not
		elif event.type == MOUSEBUTTONDOWN:
			mouseAction = pygame.mouse.get_pressed()
			if mouseAction[0]:
				currentWeapon.Shoot(player, npcList, mapLevel, frameCount, doors)

	#Animate weapon
	currentWeapon.Animate(frameCount)

	#Render Scene
	Render.renderScene(player,  mapLevel, npcList, spriteList, currentWeapon, frameCount, font, doors)

	#Draw minimap
	drawOverlay(player, npcList, mapLevel)

	#Update
	pygame.display.flip()