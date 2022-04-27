import pygame
class Button:
    def __init__(self, x, y, width, height, sprite):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.sprite = pygame.transform.scale(sprite, (self.width, self.height))
    def Draw(self, screen):
        screen.blit(self.sprite, (self.x - (self.width / 2), self.y - (self.height / 2)))
    def CheckPressed(self, mouseX, mouseY):
        return mouseX > self.x - (self.width / 2) and mouseX < self.x + (self.width / 2) and mouseY > self.y - (self.height / 2) and mouseY < self.y + (self.height / 2)
