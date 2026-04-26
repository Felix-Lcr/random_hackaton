import sys
import pygame
import config
import arena
from hero import Hero
from enemy import Enemy
import dice
import slots as slots_mod
import combat
from ui import Button

def main():
    pygame.init()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption(config.TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 22, bold=True)
    hero = Hero()
    enemy = Enemy()
    dice_row = dice.make_row()
    slots = slots_mod.make_slots()
    state = {'who': 'player', 'timer': 0, 'last_info': ''}

    def roll_all():
        hero.block = 0
        for s in slots:
            s.clear()
        for d in dice_row:
            d.selected = False
            d.assigned_to = None
            d.return_home()
            d.roll()

    def end_turn():
        combat.resolve_player_turn(hero, enemy, slots)
        state['who'] = 'enemy'
        state['timer'] = config.ENEMY_TURN_DELAY
    roll_btn = Button((config.WIDTH // 2 - 220, 500, 200, 60), 'ROULER', on_click=roll_all)
    end_btn = Button((config.WIDTH // 2 + 20, 500, 200, 60), 'FIN DU TOUR', on_click=end_turn)
    roll_all()

    def first_selected():
        return next((d for d in dice_row if d.selected), None)
    t = 0
    running = True
    while running:
        clock.tick(config.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            busy = any((d.rolling for d in dice_row))
            is_player = state['who'] == 'player'
            roll_btn.enabled = is_player and (not busy)
            end_btn.enabled = is_player and (not busy) and any((s.dice for s in slots))
            if is_player and event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1) and (not busy):
                for d in dice_row:
                    if d.assigned_to is None and d.contains(event.pos):
                        d.toggle_select()
                        break
                else:
                    sel = first_selected()
                    if sel:
                        for s in slots:
                            if s.contains(event.pos):
                                s.accept(sel)
                                break
            roll_btn.handle(event)
            end_btn.handle(event)
        if state['who'] == 'enemy':
            state['timer'] -= 1
            if state['timer'] <= 0:
                info = combat.resolve_enemy_turn(hero, enemy)
                state['last_info'] = f"{enemy.name} jette {enemy.last_roll} = {info['raw']}  (bloqué {info['absorbed']}, dégâts {info['dmg']})"
                state['who'] = 'player'
                roll_all()
        for d in dice_row:
            d.update()
        arena.draw(screen, t)
        hero.draw(screen)
        enemy.draw(screen)
        for s in slots:
            s.draw(screen)
        for d in dice_row:
            d.draw(screen)
        roll_btn.draw(screen)
        end_btn.draw(screen)
        if state['last_info']:
            t_info = font.render(state['last_info'], True, (240, 230, 210))
            screen.blit(t_info, (20, 20))
        if state['who'] == 'enemy':
            t2 = font.render("L'ennemi prépare son attaque…", True, (255, 200, 100))
            screen.blit(t2, (config.WIDTH // 2 - t2.get_width() // 2, 260))
        t += 1
        pygame.display.flip()
    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    main()
