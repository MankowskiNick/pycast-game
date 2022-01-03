#Import necessary Python libraries
import pygame, sys, math
from pygame.locals import *

#Import custom libraaries
import Render, Map, Format, Camera, NPC, LevelCreator, Sprites
from Global import *
from Render import *
from Map import *
from Format import *
from Sprites import *

#Initialize pygame
pygame.init()
mapLevel = get_level()

#Create player olbject with coords found by findPlayer
player = Camera.Camera(Format.findPlayer(mapLevel), 0)

spriteList = createSpriteList()

#Find NPCs in level data
npcList = NPC.findNPC(mapLevel)

#Set cursor to invisible
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

while True:

	#Set framerate
	clock.tick(60)
	pygame.key.set_repeat(10,10)

	#Update NPCs
	for i in range(0,len(npcList)):
		npcList[i].walk((player.x, player.y), mapLevel, npcList)

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

			#Move player according to key
			player.movePlayer(event.key, mapLevel)
			if event.key == pygame.K_m:
				mapLeveddwdal, npcList = LevelCreator.Main(player.x, player.y, mapLevel, npcList)

		#Move mouse and adjust camera angle accordingly
		elif event.type == MOUSEMOTION:
			player.angle -= (width / 2 - pygame.mouse.get_pos()[0]) / (width * 64)

			pygame.mouse.set_pos(width / 2, height / 2)


	#Render Scene
	Render.renderScene(player.x, player.y, player.angle, mapLevel, npcList, spriteList)

	#Draw minimap
	drawOverlay(player.x, player.y, player.angle, npcList, mapLevel)

	pygame.display.flip() 
	pygame.display.update()