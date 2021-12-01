#Import necessary Python libraries
import pygame, sys, math
from pygame.locals import *

#Import custom libraries
import Render, Map, Format, Camera, NPC, MapGen
from Global import *
from Render import *
from Map import *
from Format import *

#Initialize pygame
pygame.init()

#Create player object with coords found by findPlayer
player = Camera.Camera(Format.findPlayer(level), math.pi / 64)

#Find NPCs in level data
npcList = NPC.findNPC(level)
for i in range(0,len(npcList)):
	npcList[i].npcCount = len(npcList)

while True:

	#Set framerate
	clock.tick(144)
	pygame.key.set_repeat(10,10)

	#Update NPCs
	for i in range(0,len(npcList)):
		npcList[i].walk((player.x, player.y), level, npcList)

	#Cycle through each event that occurs in a frame
	for event in pygame.event.get():
		#Make sure we can exit the window
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		#Handling keyboard input
		elif event.type == KEYDOWN:
			player.movePlayer(event.key, level)

			if event.key == pygame.K_m:
				screen.fill((0,0,0))
				pygame.display.flip()
				MapGen.Main()

	#Render Scene
	Render.renderScene(player.x, player.y, player.angle, level, npcList)

	#Draw minima
	drawOverlay(player.x, player.y, player.angle, npcList, level)

	pygame.display.flip() 
	pygame.display.update()