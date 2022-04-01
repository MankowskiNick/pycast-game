#Import necessary Python libraries
import pygame, sys, math
from pygame.locals import *

#Import custom libraries
import Render, Format, Camera, NPC, LevelCreator, Sprites, Weapon, Door
from Render import *
from Weapon import *

#Initialize pygame
pygame.init()

#Create all sprite lists used by program
spriteList = createSpriteList()
boomList = createBoomList(width, height)
weaponSpriteList = createWeapSpriteList(width, height)

#Create weapon list
weaponList = createWeaponList(weaponSpriteList, boomList)

#Load map and NPC list & delete values we don't need
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

#Create font used to render numbers
font = createFont(width, height)

#What the currently selected weapon is
#currentWeapon = weaponList[0]
player.updateWeapon(weaponList[1])

#Declare framecount
frameCount = 0

#Keep track of whether or not we need to update labels
updateLabels = False

#Define sensitivity
sensitivity = 0.8

#Set cursor to invisible
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

#Set the delay between key press repeats
pygame.key.set_repeat(10,10)
while True:
	frameCount+=1

	#player.angle += 0.01
	#player.angle -= 0.01

	#Set framerate
	clock.tick(144)

	#Update NPCs
	for i in range(0,len(npcList)):
		if npcList[i].walk(player, mapLevel, npcList, doors, frameCount):

			#Cull the npc if it true
			npcList.pop(i)
			updateLabels = True
			break

	#Update npc labels
	if updateLabels:
		for n in range(0, len(npcList)):
			npcList[n].updateLabel(n)

	#Cycle through each event that occurs in a frame
	for event in pygame.event.get():

		#Make sure we can exit the window
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		#Handling keyboard input
		elif event.type == KEYDOWN:

			#Handling escape key exit
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()

			#Handle weapon selection
			if len(weaponList) <= 9 and len(weaponList) > 0:
				for i in weaponList.keys():
					if event.key == i + 48:
						player.updateWeapon(weaponList[i])

			#Move player according to key
			player.movePlayer(event.key, mapLevel, doors, npcList)

			#Open map if required
			if event.key == pygame.K_m:
				mapLevel, npcList = LevelCreator.Main(player, mapLevel, npcList, levelHIR)
				pygame.key.set_repeat(10,10)

			#Check if the doors are opened
			elif event.key == pygame.K_SPACE:
				Door.openDoor(doors, [player.x, player.y], frameCount)
		
		#Get state of mousebutton to determine whether to shoot or not
		elif event.type == MOUSEBUTTONDOWN:
			mouseAction = pygame.mouse.get_pressed()
			if mouseAction[0]:
				player.weapon.Shoot(player, npcList, mapLevel, frameCount, doors)

	#Adjust camera angle to be dependent on mouse pos	
	player.updateAngle(pygame.mouse.get_pos()[0], width, sensitivity)
	pygame.mouse.set_pos(width / 2, height / 2)
	
	#Animate weapon
	player.weapon.Animate(frameCount)
	
	#Update door animations
	for door in doors:
		door.update()

	#Render Scene
	Render.renderScene(player,  mapLevel, npcList, spriteList, player.weapon, frameCount, font, doors)

	#Update frame
	pygame.display.flip()