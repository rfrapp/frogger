import pygame
from pygame.locals import * 
from GameObject    import *

class Turtle(GameObject):

    max_frames = 6

    def __str__(self):
        return str(self.rect) 

    def __init__(self, imgPath):
        super(Turtle, self).__init__(imgPath)
        self.goes_under_water   = False
        self.is_under_water     = False
        self.last_animated_time = pygame.time.get_ticks()

    def update(self, time):
        diff = 500

        # Increase animation time if the turtle
        # is able to go underwater
        if self.goes_under_water:
            diff = 750

        if time - self.last_animated_time >= diff:
            self.current_clip += 1
            self.last_animated_time = time 

            if not self.goes_under_water and self.current_clip >= 3:
                self.current_clip = 0
            elif self.goes_under_water and self.current_clip >= 5:
                self.current_clip = 0

            if self.current_clip > 3 and self.goes_under_water:
                self.is_under_water = True 
            else:
                self.is_under_water = False 
