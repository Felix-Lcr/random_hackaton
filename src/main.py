import sys
import pygame
import config
import arena
from hero import Hero
from enemy import Enemy
import dice
from ui import Button

def main():
    pygame.init()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption(config.TITLE)
    clock = pygame.time.Clock()
    hero = Hero()
    enemy = Enemy()
    dice_row = dice.make_row()

    def roll_all():
        for d in dice_row:
            d.roll()
    roll_btn = Button((config.WIDTH // 2 - 100, 500, 200, 60), 'ROULER', on_click=roll_all)
    roll_all()
    t = 0
    running = True
    while running:
        clock.tick(config.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            roll_btn.enabled = not any((d.rolling for d in dice_row))
            roll_btn.handle(event)
        for d in dice_row:
            d.update()
        arena.draw(screen, t)
        hero.draw(screen)
        enemy.draw(screen)
        for d in dice_row:
            d.draw(screen)
        roll_btn.draw(screen)
        t += 1
        pygame.display.flip()
    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    main()
