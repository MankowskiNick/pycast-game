import pygame
from pygame.locals import *

pygame.init()

shoot = {
    1 : pygame.mixer.Sound("assets/sounds/shoot.wav"),
    2 : pygame.mixer.Sound("assets/sounds/shotgun.wav"),
    0 : pygame.mixer.Sound("assets/sounds/knife.wav"),
}
open_door = pygame.mixer.Sound("assets/sounds/door_open.wav")
pickup = {
    4000 : pygame.mixer.Sound("assets/sounds/health_pickup.wav"),
    4001 : pygame.mixer.Sound("assets/sounds/ammo_pickup.wav"),
    4002 : pygame.mixer.Sound("assets/sounds/ammo_pickup.wav"),
}

pygame.mixer.music.load("assets/sounds/step.wav")
footstep = pygame.mixer.Sound("assets/sounds/step.wav")

def Shoot_Sound(id):
    pygame.mixer.Sound.play(shoot[id])

def Door_Sound():
    pygame.mixer.Sound.play(open_door)

def Pickup_Sound(id):
    pygame.mixer.Sound.play(pickup[id])
