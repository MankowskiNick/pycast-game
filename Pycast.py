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

#Should we draw the minimap to the screen?
drawMap = True

spriteList = createSpriteList()

#Find NPCs in level data
npcList = NPC.findNPC(mapLevel)
for i in range(0,len(npcList)):
	npcList[i].npcCount = len(npcList)

while True:

	#Set framerate
	clock.tick(45)
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
			player.movePlayer(event.key, mapLevel)
			if event.key == pygame.K_m:
				mapLevel, npcList = LevelCreator.Main(player.x, player.y, mapLevel, npcList)

	#Render Scene
	Render.renderScene(player.x, player.y, player.angle, mapLevel, npcList, spriteList)

	#Draw minimap
	if drawMap:
		drawOverlay(player.x, player.y, player.angle, npcList, mapLevel)

	pygame.display.flip() 
	pygame.display.update()