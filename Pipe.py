import pygame
import random
import os 

class Pipe:
    GAP = 200
    VELOCITY = 5
    PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))

    def __init__(self,x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(self.PIPE_IMAGE, False, True)
        self.PIPE_BOTTOM = self.PIPE_IMAGE

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(40,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VELOCITY
    
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mast = bird.get_mask()
        top_pipe_mask = self.get_top_mask()
        bottom_pipe_mask = self.get_bottom_mask()

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        bottom_collision_point = bird_mast.overlap(bottom_pipe_mask, bottom_offset)
        top_collision_point = bird_mast.overlap(top_pipe_mask, top_offset)
    
        if bottom_collision_point or top_collision_point:
            return True
        else:
            return False

    def get_top_mask(self):
        return pygame.mask.from_surface(self.PIPE_TOP)

    def get_bottom_mask(self):
        return pygame.mask.from_surface(self.PIPE_BOTTOM)