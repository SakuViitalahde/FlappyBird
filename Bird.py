import pygame
import os

class Bird:
    IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),
        pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),
        pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0 
        self.img = self.IMAGES[0]
    
    def jump(self):
        self.velocity = -10,5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        # Arc movement
        movement = self.velocity * self.tick_count + 1.5 * self.tick_count**2

        # MAX SPEED
        if movement >= 16:
            movement = 16
            
        if movement < 0 :
            movement -= 2

        self.y = self.y + movement

        if movement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tick_count = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY
    
    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMAGES[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMAGES[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMAGES[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMAGES[1]
        elif self.img_count < self.ANIMATION_TIME*5:
            self.img = self.IMAGES[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.IMAGES[1]
            self.img_count = self.ANIMATION_TIME*2

        # ROTATE IMAGE FROM ITS CENTER
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        win.blit(rotated_image, new_rect.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)