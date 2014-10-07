import pygame
from pygame.locals import *
from GameObject    import *

class Croc(GameObject):
    def __init__(self, imgPath):
        super(Croc, self).__init__(imgPath)

        self.body_rect = Rect(0, 0, 80, 40)
        self.head_rect = Rect(0, 0, 39, 40)
        self.body_clip = Rect(0, 0, 80, 40)
        self.head_clips = [Rect(99, 0, 39, 40), Rect(160, 0, 37, 40)]
        self.biting    = False
        self.image.set_colorkey((0, 0, 0))
        self.current_clip = 0
        self.last_animated_time = 0
        self.startX = 0

    def move(self, xspeed, yspeed):
        self.body_rect.left += xspeed 
        self.head_rect.left += xspeed
        self.body_rect.top  += yspeed 
        self.head_rect.top  += yspeed 

    def update(self, time):

        if time - self.last_animated_time >= 750:
            self.last_animated_time = time 

            if self.current_clip == 0:
                self.current_clip = 1
                self.biting = True 
            else:
                self.current_clip = 0
                self.biting = False 

    def draw(self):
        body = self.image.subsurface(self.body_clip)
        head = self.image.subsurface(self.head_clips[self.current_clip])
        pygame.display.get_surface().blit(body, self.body_rect)
        pygame.display.get_surface().blit(head, self.head_rect)

