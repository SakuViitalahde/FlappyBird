import pygame
import neat
import time
import os
import random
from Bird import Bird

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),
pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),
pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]

PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))

def draw_window(win, bird):
    win.blit(BACKGROUND_IMAGE, (0,0))
    bird.draw(win)
    pygame.display.update()

### MAIN LOOP
def main():
    bird = Bird(200,200)
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        bird.move()
        draw_window(win, bird)
    
    pygame.quit()
    quit()

main()