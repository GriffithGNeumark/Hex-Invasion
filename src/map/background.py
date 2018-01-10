"""
   .. module: background
     :synopsis: Used to define the background on the UI.
"""

import pygame
import sys, os

"""
Controls the background on the UI that the player uses to interact
with the game.
"""
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
