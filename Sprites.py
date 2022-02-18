from re import L
import pygame
from pygame.locals import *

#Create dictionary of textures that can be easily referenced

def createSpriteList():
	spriteList = {
		#Wall Sprites
		1 : pygame.image.load("assets/walls/wall.png"),
		2 : pygame.image.load("assets/walls/window.png"),
		3 : pygame.image.load("assets/walls/trunk.png"),
		4 : pygame.image.load("assets/walls/brick1.png"),
		5 : pygame.image.load("assets/walls/brickwindow1.png"),
		6 : pygame.image.load("assets/walls/leave1.png"),
		7 : pygame.image.load("assets/walls/leave2.png"),
		8 : pygame.image.load("assets/walls/sky1.png"),
		9 : pygame.image.load("assets/walls/uglywall1.png"),
		10 : pygame.image.load("assets/walls/uglywallpainting1.png"),
		11 : pygame.image.load("assets/walls/uglywallpainting2.png"),
		12 : pygame.image.load("assets/walls/woodpainting1.png"),
		13 : pygame.image.load("assets/walls/woodpainting2.png"),

		#Doors
		900 : pygame.image.load("assets/doors/door1.png"),

		#Object Sprites
		1000 : pygame.image.load("assets/object/barrel.png"),
		1001 : pygame.image.load("assets/object/desk.png"),
		1002 : pygame.image.load("assets/object/plant1.png"),

		#NPC Sprites
		2000 : pygame.image.load("assets/npc/alive/enemy.png"),
		2001 : pygame.image.load("assets/npc/alive/npc1.png"),

		#Dead NPC Sprites
		3000 : pygame.image.load("assets/npc/dead/enemy_dead.png"),
		3001 : pygame.image.load("assets/npc/dead/npc1.png"),

		#Pickup Sprites
		4000 : pygame.image.load("assets/pickup/health_pickup.png"),
		4001 : pygame.image.load("assets/pickup/ammo_pickup.png"),
		4002 : pygame.image.load("assets/pickup/ammo_drop.png"),

	}
	return spriteList

#Create spritelist used for rendering weapons
def createWeapSpriteList(width, height):
	spriteList = {
		#Weapons sorted by ID
		1 : [pygame.image.load("assets/weapons/weapon_1/weapon_1_0.png"),pygame.image.load("assets/weapons/weapon_1/weapon_1_1.png"),pygame.image.load("assets/weapons/weapon_1/weapon_1_2.png"),pygame.image.load("assets/weapons/weapon_1/weapon_1_3.png"),],
		2 : [pygame.image.load("assets/weapons/weapon_2/weapon_2_0.png"),pygame.image.load("assets/weapons/weapon_2/weapon_2_1.png"),pygame.image.load("assets/weapons/weapon_2/weapon_2_2.png"),pygame.image.load("assets/weapons/weapon_2/weapon_2_3.png"),],
	}
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