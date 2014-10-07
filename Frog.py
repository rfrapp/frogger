import pygame, os
from pygame.locals import *
from GameObject    import *
from Timer         import *

if not pygame.mixer.get_init():
    pygame.mixer.init() # setup mixer to avoid sound lag    

class Frog(GameObject):
    max_frames              = 3
    explosion_frame_time    = 333

    def __init__(self, imgPath = ""):
        if imgPath != "":
            super(Frog, self).__init__(imgPath)
        
        self.clips = []
        self.current_clip = 0

        # explosion vars
        self.explosion_clips = []
        self.explosion_clip  = 0
        self.completed_animation  = False

        # death stuff
        self.is_alive             = True 
        self.died_by_water        = False 
        self.dead_image           = pygame.image.load(os.path.join('images', 'dead_big.png'))
        self.splash_spritesheet   = pygame.image.load(os.path.join('images', 'explosion_sprites_big.png'))
        self.splash_spritesheet.set_colorkey((0, 0, 0))
        self.dead_image.set_colorkey((0, 0, 0))

        # speeds
        self.horiz_speed          = 0
        self.original_horiz_speed = 0
        self.jump_speed           = 40
        
        # Sounds
        self.splash_sound         = pygame.mixer.Sound(os.path.join('sounds', 'splash.wav'))
        self.jump_sound           = pygame.mixer.Sound(os.path.join('sounds', 'froggerjump.ogg'))
        self.dead_sound           = pygame.mixer.Sound(os.path.join('sounds', 'froggerdie.ogg'))

        # jumping 
        self.jumping              = True 
        self.jumping_up           = False
        self.jumping_down         = False 
        self.jumping_right        = False 
        self.jumping_left         = False  
        self.jump_time            = 0

    def update(self, time):
        if not self.died_by_water:
            self.current_clip = (time - self.jump_time) / self.animation_swap_time % self.max_frames + 1
            
            if self.current_clip >= len(self.clips):
                self.current_clip = 0
        else:
            self.explosion_clip = (time - self.jump_time) / self.explosion_frame_time % self.max_frames + 1 
            if self.explosion_clip == self.max_frames:
                self.completed_animation = True 


    def is_jumping(self):
        return self.jumping_left or self.jumping_right or self.jumping_down or \
               self.jumping_up

    def draw(self):
        if self.current_clip != -1:
            img = self.image.subsurface(self.clips[self.current_clip])

            # rotate the frog according to the direction
            # the frog is jumping
            if self.jumping_right:
                img = pygame.transform.rotate(img, 270)
            elif self.jumping_down:
                img = pygame.transform.rotate(img, 180)
            elif self.jumping_left:
                img = pygame.transform.rotate(img, 90)
            else:
                self.current_clip = 0

            self.rect.width = img.get_rect().width
            self.rect.height = img.get_rect().height 

            pygame.display.get_surface().blit(img, self.rect)
        else:
            pygame.display.get_surface().blit(self.image, self.rect)

    def drawDead(self):
        if not self.died_by_water:
            # Draw the skull and crossbones
            pygame.display.get_surface().blit(self.dead_image, (self.rect.left, self.rect.top))
        else:
            # Draw the splash
            if not self.completed_animation:
                pygame.display.get_surface().blit(self.splash_spritesheet.subsurface(self.explosion_clips[self.explosion_clip]), (self.rect.left, self.rect.top))
