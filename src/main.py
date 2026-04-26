import os
import subprocess
import sys
import pygame
import config
from game import Game


KONAMI_CODE = [
    pygame.K_UP,
    pygame.K_UP,
    pygame.K_DOWN,
    pygame.K_DOWN,
    pygame.K_LEFT,
    pygame.K_RIGHT,
]


def launch_team2():
    team2_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "team2"
    )
    subprocess.Popen([sys.executable, "main.py"], cwd=team2_dir)

def main():
    pygame.init()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption(config.TITLE)
    clock = pygame.time.Clock()
    game = Game()
    t = 0
    konami_progress = []
    running = True
    while running:
        clock.tick(config.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN:
                expected_key = KONAMI_CODE[len(konami_progress)]
                if event.key == expected_key:
                    konami_progress.append(event.key)
                    if len(konami_progress) == len(KONAMI_CODE):
                        launch_team2()
                        konami_progress.clear()
                else:
                    konami_progress = [event.key] if event.key == KONAMI_CODE[0] else []
            game.handle(event)
        game.update()
        game.draw(screen, t)
        t += 1
        pygame.display.flip()
    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    main()
