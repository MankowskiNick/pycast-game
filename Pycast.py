import main, Button
import pygame, sys, configparser
from pygame.locals import *

config = configparser.ConfigParser()
config.read('settings.conf')
width = int(config['WINDOW']['width'])
height = int(config['WINDOW']['height'])
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PyCasting")
level = "level.leveldata"
inMenu = True
playGame = False

menuBGSprite = pygame.image.load("assets/system/menu/menu_bg.png")
menuTitleSprite = pygame.image.load("assets/system/menu/menu_title.png")
playButtonSprite = pygame.image.load("assets/system/menu/play_button.png")
quitButtonSprite = pygame.image.load("assets/system/menu/exit_button.png")
loadingPopupSprite = pygame.image.load("assets/system/menu/loading_popup.png")


playButton = Button.Button(width / 2, 288, 350, 125, playButtonSprite)
quitButton = Button.Button(width / 2, 438, 350, 125, quitButtonSprite)

menuBG = Button.Button(width / 2, height / 2, width, height, menuBGSprite)
menuTitle = Button.Button(width / 2, height / 2, width, height, menuTitleSprite)

loadingPopup = Button.Button(width / 2, height / 2, width / 2, 250 / 2, loadingPopupSprite)

while inMenu:
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == QUIT:
            inMenu = False
        if event.type == MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            if (quitButton.CheckPressed(mouseX, mouseY)):
                inMenu = False
                playGame = False
            if (playButton.CheckPressed(mouseX, mouseY)):
                #inMenu = False
                playGame = True
                


    menuBG.Draw(screen)
    menuTitle.Draw(screen)
    playButton.Draw(screen)
    quitButton.Draw(screen)

    if playGame:
        playGame = False
        loadingPopup.Draw(screen)
        pygame.display.flip()
        main.RunGame("level.leveldata")
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
    pygame.display.flip()


pygame.quit()
sys.exit()