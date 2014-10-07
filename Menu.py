import pygame, os, sys
from pygame.locals import *
from Frog import *

if not pygame.mixer.get_init():
    pygame.mixer.init() # setup mixer to avoid sound lag

class Menu():
    def __init__(self, width, height):
        self.width = width
        self.height = height 
        self.frogs = []
        self.top_rect = Rect(0, 0, self.width, self.height / 2)
        self.bottom_rect = Rect(0, self.height / 2, self.width, self.height / 2)
        self.items = ["Play", "How to Play", "Quit"]
        self.item_surfaces = []
        self.item_rects    = []
        self.howToPlay = ["Press escape to return to the menu", "Arrow keys = move", "p = pause", "Goal:", "Get 5 frogs to the blue holes at the top", "of the screen without dying!"]
        self.howToPlaySurfaces = []
        self.howToPlayShown = False
        self.last_frog = -1
        self.frog_changed = False
        self.open = True 
        self.background_music = pygame.mixer.Sound(os.path.join('sounds', 'froggermain.ogg'))
        self.font = pygame.font.Font(os.path.join('fonts', "FreeMonoBold.ttf"), 42)
        self.howToFont = pygame.font.Font(os.path.join('fonts', 'FreeMonoBold.ttf'), 22)
        self.letter_surfaces = []
        self.letters = -1
        self.coins   = 0

        self.title = "FROGGER"
        # Create surfaces for the letters of "FROOGGER"
        for i in range(7):
            self.letter_surfaces.append(self.font.render(self.title[i], True, (155, 255, 155)))

        # Create surfaces for each menu item
        for i in self.items:
            self.item_surfaces.append(self.font.render(i, True, (155, 255, 155)))

        # Start drawing menu options at startY
        startY = self.height / 2 + 20

        # Create rects for each menu item surface
        for i in range(len(self.items)):
            self.item_rects.append(Rect(self.width / 2 - self.item_surfaces[i].get_rect().width / 2, startY, 
                                        self.item_surfaces[i].get_rect().width, self.item_surfaces[i].get_rect().height))
            startY += 100

        # Create 7 frogs for the intro cinematic
        for i in range(7):
            frog = Frog(os.path.join('images', "frog_sprites_big.png"))
            frog.image.set_colorkey((0, 0, 0))

            # standing
            frog.clips.append(Rect(120, 0, 35, 26))
            # mid-jump
            frog.clips.append(Rect(62,  0, 26, 35))
            # full jump
            frog.clips.append(Rect(0,   0, 30, 33))

            frog.setPos((i + 1) * 65, self.height + frog.rect.height)
            # print frog.rect 

            self.frogs.append(frog)

        self.background_music.play()

        # Create surfaces for the how to play menu
        for i in self.howToPlay:
            self.howToPlaySurfaces.append(self.howToFont.render(i, True, (155, 255, 155)))

    def stopMusic(self):
        self.background_music.stop()

    def is_open(self):
        return self.open 

    def update(self):
        for i in range(len(self.frogs)):

            # Animate the frog
            self.frogs[i].update(pygame.time.get_ticks())
            
            # Move the frogs if they have not gotten to 
            # 1/5 of the height
            if self.last_frog == -1:
                self.frogs[i].move(0, -2)

            # A frog has gotten to 1/5 of the screen,
            # the rest should stop
            if self.frogs[i].rect.top <= self.height / 5 - self.frogs[i].rect.height / 2 and not self.frog_changed:
                self.last_frog += 1
                self.frog_changed = True 

    def draw(self):
        # Draw the top half of the screen in blue
        pygame.draw.rect(pygame.display.get_surface(), (0, 0, 73), self.top_rect)
        
        # Draw the bottom half of the screen in black
        pygame.draw.rect(pygame.display.get_surface(), (0, 0, 0), self.bottom_rect)

        # Draw the letters in "FROGGER"
        for i in range(self.letters):
            pygame.display.get_surface().blit(self.letter_surfaces[i], self.frogs[i].rect)

        if self.letters != len(self.frogs):
            i = 0

            while i < len(self.frogs):
                if self.frog_changed:
                    self.letters += 1
                    if self.letters > len(self.frogs):
                        self.letters -= 1 
                    self.frogs[i].is_alive = False  
                    self.frog_changed = False 
                else:
                    if self.frogs[i].is_alive:
                        self.frogs[i].draw()
                i += 1 

        # Check if all the letters are drawn
        if self.letters == len(self.frogs):
            startY = self.height / 2 + 20

            # Show the menu items if the how to play menu
            # is not open
            if not self.howToPlayShown:
                for i in range(len(self.item_surfaces)):
                    pygame.display.get_surface().blit(self.item_surfaces[i], self.item_rects[i])
            else:
                # Draw the surfaces for the how to play menu
                for i in range(len(self.howToPlaySurfaces)):
                    pygame.display.get_surface().blit(self.howToPlaySurfaces[i], (self.width / 2 - self.howToPlaySurfaces[i].get_rect().width / 2, startY))
                    startY += 50

    def handleInput(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if not self.howToPlayShown:
                # The play button was clicked
                if self.item_rects[0].collidepoint(pygame.mouse.get_pos()):
                    self.open = False 

                # The how to play button was clicked
                if self.item_rects[1].collidepoint(pygame.mouse.get_pos()):
                    self.howToPlayShown = True 

                # The quit button was clicked
                if self.item_rects[2].collidepoint(pygame.mouse.get_pos()):
                    sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.howToPlayShown = False 
