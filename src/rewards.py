import random
import pygame
import config
import dice as dice_mod
CARDS = [{'key': 'add_die', 'title': 'DÉ EN PLUS', 'desc': '+1d6 dans ton pool', 'color': (120, 200, 255)}, {'key': 'heal', 'title': 'POTION +10', 'desc': 'Récupère 10 HP', 'color': (120, 220, 140)}, {'key': 'max_hp', 'title': 'ENDURANCE', 'desc': '+8 HP max', 'color': (220, 130, 100)}, {'key': 'extra_roll', 'title': 'RELANCE BONUS', 'desc': '+1 relance par tour', 'color': (200, 220, 100)}, {'key': 'boost_slot', 'title': 'AMPLIFICATION', 'desc': '×1.2 sur tous les slots', 'color': (255, 180, 220)}]

class RewardScreen:

    def __init__(self):
        self.offered = []
        self.title_font = pygame.font.SysFont('Arial', 40, bold=True)
        self.card_title = pygame.font.SysFont('Arial', 24, bold=True)
        self.desc_font = pygame.font.SysFont('Arial', 18)

    def roll_offerings(self):
        self.offered = random.sample(CARDS, min(3, len(CARDS)))

    def _layout(self):
        n = len(self.offered)
        total_w = n * config.REWARD_CARD_W + (n - 1) * config.REWARD_GAP
        x0 = (config.WIDTH - total_w) // 2
        y0 = 220
        return [pygame.Rect(x0 + i * (config.REWARD_CARD_W + config.REWARD_GAP), y0, config.REWARD_CARD_W, config.REWARD_CARD_H) for i in range(n)]

    def handle(self, event, game):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect, card in zip(self._layout(), self.offered):
                if rect.collidepoint(event.pos):
                    apply_card(card, game)
                    return True
        return False

    def draw(self, surface):
        overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        title = self.title_font.render('CHOISIS UNE RÉCOMPENSE', True, (240, 220, 255))
        surface.blit(title, (config.WIDTH // 2 - title.get_width() // 2, 120))
        rects = self._layout()
        mouse = pygame.mouse.get_pos()
        for rect, card in zip(rects, self.offered):
            hover = rect.collidepoint(mouse)
            pygame.draw.rect(surface, config.REWARD_BG, rect, border_radius=12)
            border = card['color'] if hover else config.REWARD_BORDER
            pygame.draw.rect(surface, border, rect, 4 if hover else 2, border_radius=12)
            pygame.draw.circle(surface, card['color'], (rect.centerx, rect.y + 90), 45)
            t = self.card_title.render(card['title'], True, card['color'])
            surface.blit(t, (rect.centerx - t.get_width() // 2, rect.y + 170))
            d = self.desc_font.render(card['desc'], True, (230, 230, 240))
            surface.blit(d, (rect.centerx - d.get_width() // 2, rect.y + 210))

def apply_card(card, game):
    k = card['key']
    hero = game.hero
    if k == 'heal':
        hero.hp = min(hero.max_hp, hero.hp + 10)
    elif k == 'max_hp':
        hero.max_hp += 8
    elif k == 'add_die':
        new_count = len(game.dice_row) + 1
        game.dice_row = dice_mod.make_row(count=new_count)
    elif k == 'extra_roll':
        game.max_rerolls += 1
    elif k == 'boost_slot':
        for s in game.slots:
            s.bonus_mult *= 1.2
    game._next_fight()
