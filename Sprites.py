import pygame
from pygame.locals import *

#Create dictionary of textures that can be easily referenced

def createSpriteList():
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
	return spriteList