import sys
import pygame
import config
import arena
from hero import Hero
from enemy import Enemy
import dice

def main():
    pygame.init()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption(config.TITLE)
    clock = pygame.time.Clock()
    hero = Hero()
    enemy = Enemy()
    dice_row = dice.make_row()
    t = 0
    running = True
    while running:
        clock.tick(config.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        arena.draw(screen, t)
        hero.draw(screen)
        enemy.draw(screen)
        for d in dice_row:
            d.draw(screen)
        t += 1
        pygame.display.flip()
    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    main()
