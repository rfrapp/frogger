import pygame
from pygame.locals import *
from GameOver      import *
from Turtle        import *

class TurtleGroup():

    def __init__(self, n):
        self.turtles = []
        self.perGroup = n 

    def moveGroup(self, width):
        for i in self.turtles:
            i.move()
            i.update(pygame.time.get_ticks())

        if self.turtles[-1].rect.right < 0:
            self.turtles[-3].rect.left = width + 10
            self.turtles[-2].rect.left = width + 10 + self.turtles[-2].rect.width
            self.turtles[-1].rect.left = width + 10 + 2 * self.turtles[-1].rect.width        
