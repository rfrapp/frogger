import pygame
from pygame.locals import *

class Timer():
    def __init__(self, count_from):
        self.paused = False
        self.started = False
        self.start_ticks = 0
        self.paused_ticks = 0
        self.countdown_from = count_from 
        self.seconds = 0

    def is_started(self):
        return self.started 

    def start(self):
        self.started = True 
        self.paused = False
        self.start_ticks = pygame.time.get_ticks()

    def get_seconds(self):
        if self.started and not self.paused:
            self.seconds = self.countdown_from - ((pygame.time.get_ticks() - self.start_ticks) / 1000)
            return self.seconds
        else:
            return self.seconds 

    def toggle_pause(self):
        if self.paused:
            self.paused = False
            self.start_ticks = pygame.time.get_ticks() - self.paused_ticks
            self.paused_ticks = 0
        else:
            self.paused = True
            self.paused_ticks = pygame.time.get_ticks() - self.start_ticks 

    def reset(self):
        self.start_ticks = pygame.time.get_ticks()

    def stop(self):
        self.started = False
        self.paused  = False 

    def pause(self):
        if self.paused and not self.started:
            self.paused = True 
            self.paused_ticks = pygame.time.get_ticks() - self.start_ticks

    def unpause(self):
        if self.paused:
            self.paused = False 
            self.start_ticks = pygame.time.get_ticks() - self.paused_ticks
            self.paused_ticks = 0

    def get_ticks(self):
        if self.started:
            if self.paused:
                return self.paused_ticks
            else:
                return pygame.time.get_ticks() - self.start_ticks
