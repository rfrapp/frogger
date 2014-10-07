import pygame
from pygame.locals import *

class GameObject(object):
    
    animation_swap_time = 75

    def __init__(self):
        self.clips = []
        self.rect  = None
        self.speed = 0
        self.image = None  

    def __init__(self, imgPath): 
        self.speed = 0
        self.clips = []
        self.image = pygame.image.load(imgPath)
        self.rect  = self.image.get_rect()
        self.current_clip = 0

    def setPos(self, x, y):
        self.rect.left = x 
        self.rect.top  = y 

    def move(self, xspeed, yspeed):
        self.rect.left += xspeed
        self.rect.top  += yspeed 

    def setImage(self, image):
        self.image = image 
        self.rect = image.get_rect()
        self.current_clip = -1


    def draw(self):
        if len(self.clips) == 0:
            pygame.display.get_surface().blit(self.image, self.rect)
        else:
            if self.current_clip == 0:
                self.rect.width = self.clips[self.current_clip].width
            self.rect.height = self.clips[self.current_clip].height 
            # print self.clips 
            pygame.display.get_surface().blit(self.image.subsurface(self.clips[self.current_clip]), self.rect)