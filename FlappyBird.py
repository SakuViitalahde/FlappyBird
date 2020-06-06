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

def draw_window(win, birds, pipes, base):
    win.blit(BACKGROUND_IMAGE, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    for bird in birds:
        bird.draw(win)
    text = STAT_FONT.render(f"Score: {birds[0].score}", 1, (255,255,255))
    win.blit(text,(WIN_WIDTH - 20 - text.get_width(), 10))
    pygame.display.update()

def handle_pipes(pipes, birds, ge, nets):
    remove_pipes = []
    add_pipe = False

    for pipe in pipes:
        for index, bird in enumerate(birds):
            if pipe.collide(bird):
                ge[index].fitness -= 1

                # Remove bird and its net and genome
                birds.pop(index)
                ge.pop(index)
                nets.pop(index)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
        
        if pipe.x + pipe.PIPE_TOP.get_width() < 0:
            remove_pipes.append(pipe)
        
        pipe.move()
    
    if add_pipe:
        for bird in birds:
            bird.score += 1
        for g in ge:
            g.fitness += 5 
        pipes.append(Pipe(WIN_WIDTH + 100))

    for pipe in remove_pipes:
        pipes.remove(pipe)

### MAIN LOOP (genomes and config always needed for NEAT)
def main(genomes, config):
    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        # create net
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        #create bitrd
        birds.append(Bird(230,350))
        g.fitness = 0
        ge.append(g)

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
                pygame.quit()
                quit()

        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_index = 1
        else:
            running = False
            break

        for index, bird in enumerate(birds):
            if base.collide(bird):
                birds.pop(index)
                ge.pop(index)
                nets.pop(index)
            else:    
                bird.move()
                ge[index].fitness += 0.1

                # Active neuro net, with given input values
                # Here we use birds y position, distance to end of top pipe and distance of bird to end of bottom pipe
                output = nets[index].activate((bird.y, abs(bird.y) - pipes[pipe_index].height, abs(bird.y) - pipes[pipe_index].bottom))

                #output is list of outputs
                if output[0] > 0.5:
                    bird.jump()
            
        handle_pipes(pipes, birds, ge, nets)

        base.move()
        if len(birds) > 0:
            draw_window(win, birds, pipes, base)

def run(config_path):
    # Setup config
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    #Setup population
    population = neat.Population(config)

    # Output statistics
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Set fitness function and generation count
    winner = population.run(main, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)