import pygame
import config
import arena
from hero import Hero
from enemy import Enemy
import dice
import slots as slots_mod
import combat
from ui import Button

class Game:

    def __init__(self):
        self.hero = Hero()
        self.enemy = Enemy()
        self.dice_row = dice.make_row()
        self.slots = slots_mod.make_slots()
        self.phase = 'player'
        self.enemy_timer = 0
        self.max_rerolls = config.MAX_REROLLS_DEFAULT
        self.last_info = ''
        self.font = pygame.font.SysFont('Arial', 22, bold=True)
        self.huge = pygame.font.SysFont('Arial', 56, bold=True)
        self.roll_btn = Button((config.WIDTH // 2 - 220, 500, 200, 60), 'RELANCER', on_click=self._re_roll)
        self.end_btn = Button((config.WIDTH // 2 + 20, 500, 200, 60), 'FIN DU TOUR', on_click=self._end_turn)
        self.restart_btn = Button((config.WIDTH // 2 - 110, config.HEIGHT // 2 + 60, 220, 55), 'REJOUER', on_click=self.reset)
        self._start_turn()

    def _start_turn(self):
        self.hero.block = 0
        for s in self.slots:
            s.clear()
        for d in self.dice_row:
            d.selected = False
            d.assigned_to = None
            d.return_home()
            d.roll()
        self.rerolls_left = self.max_rerolls

    def _re_roll(self):
        if self.rerolls_left <= 0:
            return
        for d in self.dice_row:
            if d.assigned_to is None and (not d.rolling):
                d.selected = False
                d.roll()
        self.rerolls_left -= 1

    def _end_turn(self):
        combat.resolve_player_turn(self.hero, self.enemy, self.slots)
        if self.enemy.hp <= 0:
            self.phase = 'win'
            return
        self.phase = 'enemy'
        self.enemy_timer = config.ENEMY_TURN_DELAY

    def reset(self):
        self.hero = Hero()
        self.enemy = Enemy()
        for s in self.slots:
            s.clear()
        self.phase = 'player'
        self.max_rerolls = config.MAX_REROLLS_DEFAULT
        self.last_info = ''
        self._start_turn()

    def handle(self, event):
        if self.phase in ('win', 'lose'):
            self.restart_btn.handle(event)
            return
        busy = any((d.rolling for d in self.dice_row))
        is_player = self.phase == 'player'
        self.roll_btn.enabled = is_player and (not busy) and (self.rerolls_left > 0)
        self.end_btn.enabled = is_player and (not busy) and any((s.dice for s in self.slots))
        if is_player and event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1) and (not busy):
            for d in self.dice_row:
                if d.assigned_to is None and d.contains(event.pos):
                    d.toggle_select()
                    return
            sel = next((d for d in self.dice_row if d.selected), None)
            if sel:
                for s in self.slots:
                    if s.contains(event.pos):
                        s.accept(sel)
                        return
        self.roll_btn.handle(event)
        self.end_btn.handle(event)

    def update(self):
        for d in self.dice_row:
            d.update()
        if self.phase == 'enemy':
            self.enemy_timer -= 1
            if self.enemy_timer <= 0:
                info = combat.resolve_enemy_turn(self.hero, self.enemy)
                self.last_info = f"{self.enemy.name} jette {self.enemy.last_roll} = {info['raw']}  (bloqué {info['absorbed']}, dégâts {info['dmg']})"
                if self.hero.hp <= 0:
                    self.phase = 'lose'
                else:
                    self.phase = 'player'
                    self._start_turn()

    def draw(self, surface, t):
        arena.draw(surface, t)
        self.hero.draw(surface)
        self.enemy.draw(surface)
        for s in self.slots:
            s.draw(surface)
        for d in self.dice_row:
            d.draw(surface)
        self.roll_btn.label = f'RELANCER ({self.rerolls_left})'
        self.roll_btn.draw(surface)
        self.end_btn.draw(surface)
        if self.last_info:
            t_info = self.font.render(self.last_info, True, (240, 230, 210))
            surface.blit(t_info, (20, 20))
        if self.phase == 'enemy':
            t2 = self.font.render("L'ennemi prépare son attaque…", True, (255, 200, 100))
            surface.blit(t2, (config.WIDTH // 2 - t2.get_width() // 2, 260))
        if self.phase in ('win', 'lose'):
            self._draw_end(surface)

    def _draw_end(self, surface):
        overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        surface.blit(overlay, (0, 0))
        if self.phase == 'win':
            txt = self.huge.render('VICTOIRE !', True, config.GREEN)
        else:
            txt = self.huge.render('VAINCU…', True, config.RED)
        surface.blit(txt, (config.WIDTH // 2 - txt.get_width() // 2, config.HEIGHT // 2 - 80))
        self.restart_btn.draw(surface)
