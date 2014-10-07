import pygame, os, random
from Frog          import *
from pygame.locals import *
from GameObject    import *
from Turtle        import *
from Timer         import *
from Croc          import *

if not pygame.mixer.get_init():
    pygame.mixer.init() # setup mixer to avoid sound lag

pygame.font.init()
random.seed()

BARWIDTH            = 225
FROG_LIFE           = 45
FROG_HORIZ_JUMP     = 40
NUM_FROGS           = 9
LANE_HEIGHT         = 40
MARGIN_FROM_HUD     = 60
turtle_group_margin = 200
LOG_MARGIN          = 225
MAX_LEVELS          = 3

class MainGame(object):

    # Creates and initializes all member
    # variables
    def initVars(self):
        self.width                = 0
        self.height               = 0

        # Objects for Cars, Logs, Frogs, and Turtles
        self.cars                 = []
        self.logs                 = []
        self.frogs                = []
        self.winning_frogs        = []
        self.dead_frogs           = []
        self.turtles              = []
        
        self.fly                  = GameObject(os.path.join('images', "fly_big.png"))
        self.fly.image.set_colorkey((0, 0, 0))
        self.fly_appear_time      = 12
        self.fly_appear_timer     = Timer(self.fly_appear_time)
        self.fly_timer            = Timer(self.fly_appear_time / 2)

        self.croc                 = Croc(os.path.join('images', "croc_sprites_big.png"))

        # Background
        self.background           = pygame.image.load(os.path.join('images', "background.png"))
        self.background_music     = pygame.mixer.Sound(os.path.join('sounds','bgmusic.ogg'))
        self.frog_win_sound       = pygame.mixer.Sound(os.path.join('sounds', 'frogwin.ogg'))
        self.frog_win_sound.set_volume(1000)

        # Vars for UI element data
        self.score                = 0
        self.timeSinceNew         = 0
        self.level                = 1
        self.message              = ""

        # Surfaces for UI elements
        self.scoreSurface         = None
        self.levelSurface         = None 
        self.timeRemainingSurface = None
        self.liveSurface = pygame.image.load(os.path.join("images", "safe_frog_big.png")).subsurface(Rect(0, 0, 40, 35))
        self.messageSurface       = None

        # Rects
        self.timeRemainingRect    = Rect(0, 10, BARWIDTH, 22)
        self.goalRects            = []

        # More pygame stuff. Timer and font
        self.clock                = pygame.time.Clock()
        self.font                 = pygame.font.Font(os.path.join('fonts', "FreeMonoBold.ttf"), 22)

        self.carSpeed             = 1
        self.num_logs             = 3
        self.lives                = 5

        self.frog_died            = False 
        self.frog_won             = False 
        self.game_over            = False
        self.level_complete       = False 
        self.fly_shown            = False 
        self.level_complete_time  = 0
        self.paused               = False 
        self.croc_in_level        = False 
        self.back_to_menu         = False 

        self.timer                = Timer(FROG_LIFE)
        self.game_over_time       = 0

        self.powerup_time         = 3
        self.powerup_timer        = Timer(self.powerup_time)

    # Returns whether or not the game is
    # ready to return to the menu
    def is_over(self):
        return self.back_to_menu

    # Returns whether or not the game is paused
    def is_paused(self):
        return self.paused 

    # Starts the timer and plays the background
    # music
    def startGame(self):
        self.background_music.play(-1)
        self.timer.start()

    # stops the background music
    def endGame(self):
        self.background_music.stop()

    def __init__(self, w, h):
        self.initVars()

        self.width = w
        self.height = h 

        self.timeRemainingRect.left = self.width / 2 - self.timeRemainingRect.width / 2 - 20

        self.initializeElements()

    # Used to kill the current frog
    # Plays a death animation depending on 
    # the method of death
    def killFrog(self):
        self.frogs[0].is_alive = False

        if not self.frogs[0].died_by_water:
            self.frogs[0].dead_sound.play()
        else:
            self.frogs[0].splash_sound.play()

        self.frogs[0].dead_time = pygame.time.get_ticks()
        self.frog_died = True 
        self.frog_won  = False 

    # Creates the game objects (cars, turtles, etc)
    # based on the level
    def initializeElements(self):
        self.cars          = []
        self.logs          = []
        self.frogs         = []
        self.winning_frogs = []
        self.dead_frogs    = []
        self.turtles       = []
        self.frog_died     = False 
        self.frog_won      = False 

        # Create the frogs
        self.initFrogs()

        if self.level == 1:
            # Create the cars
            self.initCarRow(2, 40, 0,   0, 10)
            self.initCarRow(3, 40, 60,  0, -5)
            self.initCarRow(4, 70, 126, 1, -20)
            self.initCarRow(5, 40, 220, 1, 45)
            self.initCarRow(6, 40, 280, 0, 20)

            self.initTurlesInRow(8, 3)
            self.initTurlesInRow(12, 3)

            self.initLogsInRow(9)
            self.initLogsInRow(10, True)
            self.initLogsInRow(11)
        elif self.level == 2:
            # Create the cars
            self.initCarRow(2, 40, 0,   0, 10)
            self.initCarRow(3, 40, 60,  0, -5)
            self.initCarRow(4, 70, 126, 1, -20)
            self.initCarRow(5, 40, 220, 1, 45)
            self.initCarRow(6, 40, 280, 0, 20)

            self.initTurlesInRow(8, 3)
            self.initTurlesInRow(11, 3)

            self.initLogsInRow(9)
            self.initLogsInRow(10, True)
            self.initLogsInRow(12, False, True)
        elif self.level == 3:
            # Create the cars
            self.initCarRow(2, 40, 0,   0, 10)
            self.initCarRow(3, 40, 60,  0, -5, 2)
            self.initCarRow(4, 70, 126, 1, -20)
            self.initCarRow(5, 40, 220, 1, 45)
            self.initCarRow(6, 40, 280, 0, 20, 2)

            self.initTurlesInRow(8, 3)
            self.initTurlesInRow(11, 3)

            self.initLogsInRow(9, False, True, 3)
            self.initLogsInRow(10, True)
            self.initLogsInRow(12, False, True, 3)

        self.initGoalRects()

    # Creates the rectangles for the goals
    def initGoalRects(self):
        r = Rect(24, 80, 33, 34)
        self.goalRects.append(r)
        r = Rect(144, 80, 33, 34)
        self.goalRects.append(r)
        r = Rect(264, 80, 33, 34)
        self.goalRects.append(r)
        r = Rect(384, 80, 33, 34)
        self.goalRects.append(r)
        r = Rect(504, 80, 33, 34)
        self.goalRects.append(r)

    # Creates 10 frogs 
    def initFrogs(self):
        for i in range(NUM_FROGS):
            frog = Frog(os.path.join('images', "frog_sprites_big.png"))
            frog.image.set_colorkey((0, 0, 0))

            # standing
            frog.clips.append(Rect(120, 0, 35, 26))
            # mid-jump
            frog.clips.append(Rect(62,  0, 26, 35))
            # full jump
            frog.clips.append(Rect(0,   0, 30, 33))

            frog.explosion_clips.append(Rect(114, 0, 41, 40))
            frog.explosion_clips.append(Rect(56 , 0, 41, 40))
            frog.explosion_clips.append(Rect(0  , 0, 41, 40))

            frog.setPos(self.width / 2 - 30, self.height - 95)
            self.frogs.append(frog)

    # Creates turtles positioned in a certain row
    def initTurlesInRow(self, row, perGroup, groups = 3):
        rand_group = random.randrange(groups)

        # create turtles in eighth row
        for i in range(groups):
            x = ((groups + 5) * 40) + (turtle_group_margin * i)
            y = self.getYforRow(row)

            for j in range(perGroup):
                turtle = Turtle("images/turtle_sprites_big.png")
                turtle.image.set_colorkey((0, 0, 0))
                
                if i == rand_group:
                    turtle.goes_under_water = True 

                # main
                turtle.clips.append(Rect(0, 0, 32, 35))
                # swimming half
                turtle.clips.append(Rect(56, 0, 40, 35))
                # swimming full
                turtle.clips.append(Rect(116, 0, 40, 35))
                # underwater half
                turtle.clips.append(Rect(204, 0, 35, 35))
                # underwater full
                turtle.clips.append(Rect(260, 0, 35, 35)) 
                turtle.speed = -1

                turtle.setPos(x + turtle.clips[1].width * j + 5, y)
                self.turtles.append(turtle)

    # Creates logs (big or small) positioned in a certain row
    # A crocodile could also be added to the row if "croc" is true
    def initLogsInRow(self, row, bigLogs = False, croc = False, logSpeed = 2):
        startLogs = self.num_logs
        
        if croc:
            # startLogs -= 1
            self.croc.speed = logSpeed

        if not bigLogs:
            crocX = 0
            crocY = 0

            for i in range(startLogs):
                log = GameObject("images/log_big.png")
                log.image.set_colorkey((0, 0, 0))
                x = self.width / 2 - i * LOG_MARGIN - row * 10
                y = self.getYforRow(row)
                log.setPos(x, y)
                log.speed = logSpeed

                self.logs.append(log)

                if i == startLogs - 1:
                    crocX = self.width / 2 - startLogs * LOG_MARGIN - row * 10
                    crocY = y 

                    self.croc.body_rect.left = crocX
                    self.croc.body_rect.top  = crocY
                    self.croc.head_rect.left = crocX + 80
                    self.croc.head_rect.top  = crocY 
                    self.croc_in_level = True 
        else:
            for i in range(self.num_logs - 1):
                log = GameObject("images/log_bigger.png")
                c = log.image.get_at((0, 0))
                log.image.set_colorkey(c)
                x = self.width / 2 - i * (LOG_MARGIN + log.rect.width) - i * LOG_MARGIN
                y = self.getYforRow(row)
                log.setPos(x, y)
                log.speed = logSpeed - 1

                self.logs.append(log)                  

    # Creates a car in a certain row
    # The specific car is determined by using the startx and width 
    # variables with an offset 
    def initCarRow(self, row, width, startX, direction = 0, offset = 0, speed = 0):
        for i in range(4):
            car = GameObject("images/car_sprites_big.png")
            car.clips = []
            car.image.set_colorkey((0, 0, 0))

            # main clip
            car.clips.append(Rect(startX, 0, width, 35))
            car.setPos(i * 150 + offset, self.getYforRow(row))

            if direction == 0:
                car.speed = self.carSpeed 
            else:
                car.speed = -self.carSpeed 

            if speed != 0:
                car.speed = speed 

            self.cars.append(car)

    # Moves all game objects
    def moveObjects(self):
        # Move the cars
        for car in self.cars:
            if car.speed == 0:
                car.speed = -self.carSpeed 

            car.move(car.speed, 0)

            # Checks if a leftbound car goes out of the screen
            if car.rect.right <= -1 and car.speed < 0:
                car.rect.left = self.width + 150

            # Checks if a rightbound car goes out of the screen
            elif car.rect.left >= self.width and car.speed > 0:
                car.rect.left = -150

            if len(self.frogs) >= 1:
                # Check if a car hit the frog
                if self.frogs[0].rect.colliderect(car.rect) and self.frogs[0].is_alive:
                    # The frog is dead. -1 life
                    self.killFrog()
                    carHitFrog = True 

        # Move the logs
        frogOnObject = False 
        frogSpeed = 0

        for log in self.logs:
            log.move(log.speed, 0)

            # Checks if a log has gone out of the screen
            if log.rect.left > self.width:
                log.rect.left = -LOG_MARGIN - log.rect.width 

            # Checks if the frog is on a log
            if len(self.frogs) >= 1:
                if self.frogs[0].rect.colliderect(log.rect):
                    frogOnObject = True 
                    self.frogs[0].horiz_speed = log.speed 


        # Move the turtles
        frogFellInWater = False 

        for turtle in self.turtles:
            turtle.move(turtle.speed, 0)

            # Animates the turtles
            turtle.update(pygame.time.get_ticks())  

            # Checks if a turtle went off the screen
            if turtle.rect.right < 0:
                turtle.rect.left = self.width + 10

            if len(self.frogs) >= 1:
                # Check if the frog is on a turtle
                if self.frogs[0].rect.colliderect(turtle.rect):
                    if not turtle.is_under_water:
                        frogOnObject = True
                        self.frogs[0].horiz_speed = turtle.speed 
                    elif not frogFellInWater:
                        self.frogs[0].died_by_water = True 
                        self.killFrog()
                        frogFellInWater = True
                       
        if self.croc_in_level:
            # Animates the crocodile
            self.croc.update(pygame.time.get_ticks())
            self.croc.move(self.croc.speed, 0)

            # Checks if the crocodile goes off the screen
            if self.croc.body_rect.left > self.width:
                self.croc.body_rect.left = self.logs[-1].rect.left - LOG_MARGIN
                self.croc.head_rect.left = self.logs[-1].rect.left - LOG_MARGIN + 80

            # Checks if the frog is on the crocodile
            if self.croc.body_rect.colliderect(self.frogs[0].rect) and \
               not self.croc.head_rect.colliderect(self.frogs[0].rect):

               self.frogs[0].horiz_speed = self.croc.speed 
               frogOnObject = True 
               frogOnCroc   = True 

            # Checks if the frog is on the crocodile's 
            # head. If so, the frog dies
            elif self.croc.head_rect.colliderect(self.frogs[0].rect) \
                 and self.croc.biting:
                self.killFrog()

        # If a frog is on a log or turtle, move the frog with it
        if frogOnObject and self.frogs[0].is_alive:
            self.frogs[0].move(self.frogs[0].horiz_speed, 0)

            # Check if the frog has gone out of bounds.
            # If so, the frog dies
            if self.frogs[0].rect.right < 0 or self.frogs[0].rect.left > self.width:
                self.killFrog()

    def placePowerups(self):

        # Place the fly in a goal every 12 seconds
        if self.fly_appear_timer.get_seconds() == 0 and not self.fly_shown:
            self.fly_timer.start()

            # place the fly in a random goal rectangle
            r = self.goalRects[random.randrange(len(self.goalRects))]

            # check if the rectangle picked is already taken up
            unoccupied = True  

            for i in self.winning_frogs:
                if i.rect.colliderect(r):
                    unoccupied = False 

            # Place the fly in a goal that is not 
            # taken up by a frog
            while not unoccupied:
                unoccupied = True 
                r = self.goalRects[random.randrange(len(self.goalRects))]

                for i in self.winning_frogs:
                    if i.rect.colliderect(r):
                        unoccupied = False 


            # Place the fly and tell draw() to draw it
            self.fly.rect.left = r.left + 2
            self.fly.rect.top  = r.top + 2
            self.fly_shown = True 

        # Hide the fly 6 seconds after being shown
        elif self.fly_timer.get_seconds() == 0 and self.fly_shown:
            self.fly_shown = False 
            self.fly_appear_timer.reset()


    # Checks if the game is over,
    # Changes the timer,
    # Toggles the fly
    # Handles other logic
    def play(self):

        if not self.fly_appear_timer.is_started():
            self.fly_appear_timer.start()

        # End the game if the player is out of lives
        if self.lives == 0:
            self.message = "Game over. You need more practice."
            self.messageSurface = self.font.render(self.message, True, (255, 255, 255))
            self.game_over = True 
            if self.game_over_time == 0:
                self.game_over_time = pygame.time.get_ticks()
            
            self.timer.toggle_pause()

        # End the game if the level limit has been reached
        if self.level >= MAX_LEVELS:
            self.game_over = True 
            self.message = "For more levels, send $10 to rfrapp@gmail.com"
            self.messageSurface = self.font.render(self.message, True, (255, 255, 255))

            if self.game_over_time == 0:
                self.game_over_time = pygame.time.get_ticks()

        self.timeSinceNew = self.timer.get_seconds()

        # Check if the timer ran out
        if self.timeSinceNew == 0:
            # frog will die, new one spawn
            self.killFrog()
            self.timer.reset()
            pass 

        if len(self.frogs) > 0:
            # Play the frog's animation if it's jumping
            if self.frogs[0].jumping or self.frogs[0].died_by_water:
                self.frogs[0].update(pygame.time.get_ticks())

                if self.frogs[0].current_clip == self.frogs[0].max_frames - 1:
                    # self.frogs[0].reset_jump_flags()
                    self.frogs[0].jumping = False 

        self.moveObjects()
        self.placePowerups()

    # Helper function.
    # Calculates the starting y value for a row
    def getYforRow(self, row):
        return self.height - MARGIN_FROM_HUD - row * LANE_HEIGHT

    # Draw the objects for this game mode
    def draw(self):

        pygame.display.get_surface().blit(self.background, (0, 60))
        
        # create UI surfaces
        self.levelSurface         = self.font.render("Level " + str(self.level), True, (155, 255, 155))
        self.timeRemainingSurface = self.font.render(str(self.timeSinceNew), True, (155, 255, 155))
        self.scoreSurface         = self.font.render("Score: " + str(self.score), True, (155, 255, 155))

        # adjust bar rect width
        self.timeRemainingRect.w  = (BARWIDTH / FROG_LIFE) * self.timeSinceNew

        # draw UI surfaces
        pygame.display.get_surface().blit(self.levelSurface, (self.width / 2 + 170, 10))
        pygame.display.get_surface().blit(self.timeRemainingSurface, (self.width / 2 - BARWIDTH + 50, 10))
        pygame.display.get_surface().blit(self.scoreSurface, (10, self.height - 42))
        pygame.draw.rect(pygame.display.get_surface(), (155, 255, 155), self.timeRemainingRect)

        for turtle in self.turtles:
            turtle.draw()

        for log in self.logs:
            log.draw()

        if self.fly_shown:
            self.fly.draw()

        if self.croc_in_level:
            self.croc.draw()

        if len(self.frogs) >= 1 and self.lives > 0:
            if self.frogs[0].is_alive:
                self.frogs[0].draw()
            else:
                self.frogs[0].drawDead()

                # Wait 1 second to spawn a new frog
                if pygame.time.get_ticks() - self.frogs[0].dead_time >= 1000:
                    self.dead_frogs.append(self.frogs[0])
                    self.frogs = self.frogs[1:]
                    self.frog_death_time = 0
                    self.lives -= 1
                    self.timer.reset()

        for car in self.cars:
            car.draw()

        for i in range(self.lives):
            x = self.width - 50 - (i * 40) - (10 * i)
            y = self.height - 50
            pygame.display.get_surface().blit(self.liveSurface, (x, y))

        for frog in self.winning_frogs:
            frog.draw()

        if self.level_complete or self.game_over or self.paused:
            pygame.display.get_surface().blit(self.messageSurface, 
                                             (self.width / 2 - self.messageSurface.get_rect().width / 2, 
                                              self.height / 2 - self.messageSurface.get_rect().height / 2))

            if self.level_complete and pygame.time.get_ticks() - self.level_complete_time >= 3000:
                self.level_complete = False
                self.game_over = False  
                self.level_complete_time += 3000
                self.level += 1
                self.initializeElements()
                self.timer.reset()

            if self.game_over and pygame.time.get_ticks() - self.game_over_time >= 3000:
                self.back_to_menu = True 

    # Checks whether or not the frog is in the 
    # water
    def frogInWater(self):
        on_float = False 

        for turtle in self.turtles:
            if self.frogs[0].rect.colliderect(turtle.rect):
                on_float = True 

        for log in self.logs:
            if self.frogs[0].rect.colliderect(log.rect):
                on_float = True 

        if self.croc_in_level:
            if self.frogs[0].rect.colliderect(self.croc.body_rect) \
               or self.frogs[0].rect.colliderect(self.croc.head_rect):
                on_float = True 

        return not on_float 

    # Handle input for this game mode
    def handleInput(self, event):
        moved = False 
        alive = False

        # The y value of the first row of water
        y = self.getYforRow(7)
        goal_y = self.getYforRow(12)
        
        if event.type == KEYDOWN:
            if event.key == K_UP and self.frogs[0].is_alive:

                # Keep the frog in-bounds
                if self.frogs[0].rect.top - LANE_HEIGHT > 60:
                    self.frogs[0].jump_time = pygame.time.get_ticks()
                    self.frogs[0].rect.top -= LANE_HEIGHT
                    
                    self.frogs[0].jumping_right = False 
                    self.frogs[0].jumping_left  = False 
                    self.frogs[0].jumping_down  = False
                    self.frogs[0].jumping_up    = True  

                    # Check if the frog is between the water and the goal
                    # rows
                    if self.frogs[0].rect.top <= y and self.frogs[0].rect.top > goal_y:
                        alive = not self.frogInWater()
                    else: 
                        alive = True 
                        moved = True 

                        if self.frogs[0].rect.top <= goal_y:
                            frogInRect = False 

                            # Loop through goal rects
                            for r in self.goalRects:
                                # Get center of rect
                                r_center = [(r.left + r.right) / 2.0, (r.top + r.bottom) / 2.0]

                                # Get center of frog rect
                                # print "frogs:", len(self.frogs)
                                f_center = [(self.frogs[0].rect.left + self.frogs[0].rect.right) / 2.0,
                                            (self.frogs[0].rect.top + self.frogs[0].rect.bottom) / 2.0]

                                # Get the distance between the two centers
                                distance = ((f_center[0] - r_center[0]) ** 2 + (f_center[1] - r_center[1]) ** 2) ** 0.5

                                if distance < self.frogs[0].rect.width / 2:
                                    spaceTaken = False 

                                    # Check winning frog rects to see if they collide with goal rects
                                    for f in self.winning_frogs:
                                        if r.colliderect(f.rect):
                                            spaceTaken = True 

                                    if not spaceTaken:
                                        self.frog_win_sound.play()

                                        frogInRect = True 
                                        # The frog made it to the jump
                                        frog = Frog()
                                        frog.setImage(pygame.image.load("images/safe_frog_big.png").subsurface(Rect(0, 0, 40, 35)))
                                        frog.image.set_colorkey((0, 0, 0))
                                        frog.setPos(r.left - 4, r.top)
                                        frog.winning_time = pygame.time.get_ticks()
                                        self.winning_frogs.append(frog)

                                        if self.fly.rect.colliderect(frog.rect) and self.fly_shown:
                                            self.score += 100

                                        self.frog_won = True 
                                        self.frog_died = False 

                                        if len(self.frogs) > 1:
                                            self.frogs = self.frogs[1:]
                                        
                                        self.score += 200

                                        # Level complete
                                        if len(self.winning_frogs) == 5:
                                            if self.level + 1 <= MAX_LEVELS:
                                                self.level_complete = True 
                                                self.level_complete_time = pygame.time.get_ticks()
                                                self.message = "Level complete"
                                                self.messageSurface = self.font.render(self.message, True, (255, 255, 255))
                                        else:
                                            self.timer.reset()

                            # If a frog was already in the goal space
                            if not frogInRect:
                                self.killFrog()
                    if alive:
                        self.score += 10
                        moved = True
                    else:
                        self.frogs[0].died_by_water = True 
                        self.killFrog()

            if event.key == K_DOWN and self.frogs[0].is_alive:

                # Keep the frog in-bounds 
                if self.frogs[0].rect.top + LANE_HEIGHT < self.height - 60:
                    self.frogs[0].jump_time = pygame.time.get_ticks()
                    self.frogs[0].rect.top += LANE_HEIGHT

                    self.frogs[0].jumping_right = False 
                    self.frogs[0].jumping_left  = False 
                    self.frogs[0].jumping_down  = True
                    self.frogs[0].jumping_up    = False 

                    if self.frogs[0].rect.top <= y:
                        alive = not self.frogInWater()
                    else: 
                        alive = True 
                        moved = True 

                    if alive:
                        self.score += 10
                        moved = True
                    else:
                        self.frogs[0].died_by_water = True 
                        self.killFrog()

            if event.key == K_LEFT and self.frogs[0].is_alive:
                w = FROG_HORIZ_JUMP

                # Keep the frog in-bounds 
                if self.frogs[0].rect.left - w > 0:
                    self.frogs[0].jump_time = pygame.time.get_ticks() 
                    self.frogs[0].rect.left -= w 

                    self.frogs[0].jumping_right = False 
                    self.frogs[0].jumping_left  = True 
                    self.frogs[0].jumping_down  = False
                    self.frogs[0].jumping_up    = False 

                    if self.frogs[0].rect.top <= y: 
                        alive = not self.frogInWater()
                    else: 
                        alive = True 

                    if alive:
                        moved = True
                    else:
                        self.frogs[0].died_by_water = True 
                        self.killFrog() 

            if event.key == K_RIGHT and self.frogs[0].is_alive:
                w = FROG_HORIZ_JUMP

                # Keep the frogs in-bounds
                if self.frogs[0].rect.right + w < self.width:
                    self.frogs[0].jump_time = pygame.time.get_ticks()
                    self.frogs[0].rect.left += w
                    
                    self.frogs[0].jumping_right = True 
                    self.frogs[0].jumping_left  = False 
                    self.frogs[0].jumping_down  = False
                    self.frogs[0].jumping_up    = False 

                    y = self.height - MARGIN_FROM_HUD - 7 * LANE_HEIGHT
                    alive = False

                    if self.frogs[0].rect.top <= y:
                        alive = not self.frogInWater()
                    else:
                        alive = True 

                    if alive:
                        moved = True
                    else:
                        self.frogs[0].died_by_water = True 
                        self.killFrog() 
            if event.key == K_p:
                self.timer.toggle_pause()

                if not self.paused: 
                    self.paused         = True
                    self.message        = "Paused"
                    self.messageSurface = self.font.render(self.message, True, (255, 255, 255))
                else:
                    self.paused = False 
            if moved:
                self.frogs[0].jump_sound.play()
                self.frogs[0].jumping = True 
