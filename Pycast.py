import main
import pygame, configparser
from pygame.locals import *

class Button:
    def __init__(self, x, y, width, height, sprite):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.sprite = sprite
    def Draw(self, screen):
        screen.blit(self.sprite, (self.x - (self.width / 2), self.y - (self.height / 2)))
    def CheckPressed(self, mouseX, mouseY):
        return mouseX > self.x - (width / 2) and mouseX < self.x + (width / 2) and mouseY > self.y - (self.height / 2) and mouseY < self.y + (self.height / 2)

config = configparser.ConfigParser()
config.read('gfx.conf')
width = int(config['WINDOW']['width'])
height = int(config['WINDOW']['height'])
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PyCasting")
level = "level.leveldata"
inMenu = True

quitButtonSprite = pygame.transform.scale(pygame.image.load("assets/object/1000.png"), (200, 50))


quitButton = Button(width / 2, height / 2, 200, 50, quitButtonSprite)

while inMenu:
    for event in pygame.event.get():
        if event.type == QUIT:
            inMenu = False
        if event.type == MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            if (quitButton.CheckPressed(mouseX, mouseY)):
                inMenu = False

    quitButton.Draw(screen)
    pygame.display.flip()

main.RunGame("level.leveldata")