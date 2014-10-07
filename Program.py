import pygame, sys
from pygame.locals import * 
from GameObject    import *
from MainGame      import *
from Menu          import *  

WIDTH  = 560
HEIGHT = 660

# Controls the flow of the game
class Program():

    # Booleans to distinguish which game mode you're playing
    isClassicMode = False 

    # Class to handle gameplay in classic mode
    classicMode = MainGame(WIDTH, HEIGHT)

    # The game menu
    menu = Menu(WIDTH, HEIGHT)

    # The screen, for to drawz stuff on
    screen = pygame.display.set_mode([WIDTH, HEIGHT])

    # The clock, used to regulate frame rate
    clock = pygame.time.Clock()

    def __init__(self):
        pygame.init()

    def execute(self):
        while 1:
            # The menu was just closed
            # Start the game
            if not self.menu.is_open() and not self.isClassicMode:
                self.isClassicMode = True 
                self.menu.stopMusic()
                self.classicMode.startGame()

            # The game ended, go back to the menu and reset the game
            if self.classicMode.is_over():
                self.isClassicMode = False 
                self.classicMode.endGame()
                self.classicMode = MainGame(WIDTH, HEIGHT)
                self.menu = Menu(WIDTH, HEIGHT)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if self.isClassicMode: 
                    self.classicMode.handleInput(event)
                else:
                    self.menu.handleInput(event)

            if self.isClassicMode and not self.classicMode.is_paused():
                self.classicMode.play()
            else:
                self.menu.update()

            self.screen.fill([0, 0, 0])

            if self.isClassicMode:
                self.classicMode.draw()
            else:
                self.menu.draw()

            pygame.display.flip()

            # regulate the frame rate to 60 fps
            self.clock.tick(60)
