import pygame, configparser, sys
from pygame.locals import *

#Create dictionary of textures that can be easily referenced

def createSpriteList():
	
	#Read sprites from config file
	spriteList = {}
	gfxConfig = configparser.ConfigParser()
	gfxConfig.read('settings.conf')
	for option in gfxConfig['SPRITES']:
		spriteList[int(option)] = pygame.image.load(gfxConfig['SPRITES'][option])

	return spriteList

#Create spritelist used for rendering weapons
def createWeapSpriteList(width, height):

	#Read sprites from config file
	spriteList = {}
	gfxConfig = configparser.ConfigParser()
	gfxConfig.read('settings.conf')
	for option in gfxConfig['WEAPON_SPRITES']:
		currentSprites = gfxConfig['WEAPON_SPRITES'][option].split(', ')
		currentList = []
		for i in range(0,len(currentSprites)):
			currentList.append(pygame.image.load(currentSprites[i]))

		spriteList[int(option)] = currentList

	#Resize images to appropriate size
	for i in range(0,len(spriteList.keys())):
		for n in range(0,len(spriteList[list(spriteList.keys())[i]])):
			spriteList[list(spriteList.keys())[i]][n] = pygame.transform.scale(spriteList[list(spriteList.keys())[i]][n], (width, height))
	return spriteList

#Create texture list for the "flash" when a gun is fired
def createBoomList(width, height):
	spriteList = [
		#3 Frame long blast when weapon is fired
		pygame.image.load("assets/weapons/blast/blast_1.png"),
		pygame.image.load("assets/weapons/blast/blast_2.png"),
		pygame.image.load("assets/weapons/blast/blast_3.png"),
	]
	for i in range(0,len(spriteList)):
		spriteList[i] = pygame.transform.scale(spriteList[i], (width, height))
	return spriteList

#Create font used to show ammo count and hp
def createFont(width, height):
	spriteList = [
		pygame.image.load("assets/system/font/0.png"),
		pygame.image.load("assets/system/font/1.png"),
		pygame.image.load("assets/system/font/2.png"),
		pygame.image.load("assets/system/font/3.png"),
		pygame.image.load("assets/system/font/4.png"),
		pygame.image.load("assets/system/font/5.png"),
		pygame.image.load("assets/system/font/6.png"),
		pygame.image.load("assets/system/font/7.png"),
		pygame.image.load("assets/system/font/8.png"),
		pygame.image.load("assets/system/font/9.png"),
	]
	for i in range(0,len(spriteList)):
		spriteList[i] = pygame.transform.scale(spriteList[i], (1 * width / 32, 2 * height / 24))
	return spriteList