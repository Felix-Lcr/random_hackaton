import sys
import pygame
import config
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption(config.TITLE)
    clock = pygame.time.Clock()
    game = Game()
    t = 0
    running = True
    while running:
        clock.tick(config.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            game.handle(event)
        game.update()
        game.draw(screen, t)
        t += 1
        pygame.display.flip()
    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    main()
