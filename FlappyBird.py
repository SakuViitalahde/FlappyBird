import pygame
import neat
import time
import os
import random
from Bird import Bird
from Pipe import Pipe
from Base import Base

pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))
STAT_FONT = pygame.font.SysFont("comicsains", 50)

def draw_window(win, bird, pipes, base):
    win.blit(BACKGROUND_IMAGE, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    bird.draw(win)
    text = STAT_FONT.render(f"Score: {bird.score}", 1, (255,255,255))
    win.blit(text,(WIN_WIDTH - 20 - text.get_width(), 10))
    pygame.display.update()

def handle_pipes(pipes, bird):
    remove_pipes = []
    add_pipe = False

    for pipe in pipes:
        if pipe.collide(bird):
            pass
        if pipe.x + pipe.PIPE_TOP.get_width() < 0:
            remove_pipes.append(pipe)

        if not pipe.passed and pipe.x < bird.x:
            pipe.passed = True
            add_pipe = True
        
        pipe.move()
    
    if add_pipe:
        bird.score += 1
        pipes.append(Pipe(WIN_WIDTH + 100))

    for pipe in remove_pipes:
        pipes.remove(pipe)

### MAIN LOOP
def main():
    bird = Bird(230,350)
    base = Base(730)
    pipes = [Pipe(WIN_WIDTH + 100)]
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        bird.move()
        handle_pipes(pipes, bird)
        base.collide(bird)
        base.move()
        draw_window(win, bird, pipes, base)
    
    pygame.quit()
    quit()

main()