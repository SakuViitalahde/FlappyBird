import pygame
import os

class Base:
    VELOCITY = 5
    BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
    WIDTH = BASE_IMAGE.get_width()

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY


        # ground is 2 images
        # after image is out of screen move it behind the other image
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    
    def draw(self, win):
        win.blit(self.BASE_IMAGE,(self.x1, self.y))
        win.blit(self.BASE_IMAGE,(self.x2, self.y))

    def collide(self, bird):
        if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
            return True