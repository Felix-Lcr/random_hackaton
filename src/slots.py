import pygame
import config
import assets_loader
_icon_cache = {}

def _icon(kind):
    if kind not in _icon_cache:
        _icon_cache[kind] = assets_loader.load_image(f'slot_{kind}.png', size=(config.SLOT_ICON, config.SLOT_ICON))
    return _icon_cache[kind]

class Slot:

    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.w = config.SLOT_W
        self.h = config.SLOT_H
        self.kind = kind
        self.dice = []

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    @property
    def color(self):
        return {'attack': config.ATTACK_COLOR, 'defense': config.DEFENSE_COLOR, 'heal': config.HEAL_COLOR}[self.kind]

    @property
    def total(self):
        return sum((d.value for d in self.dice))

    def contains(self, pos):
        return self.rect.collidepoint(pos)

    def accept(self, die):
        self.dice.append(die)
        die.selected = False
        die.assigned_to = self
        offset = (len(self.dice) - 1) * 18
        die.x = self.rect.centerx - die.size // 2 + offset
        die.y = self.rect.centery - die.size // 2 - 4 - offset

    def clear(self):
        for d in self.dice:
            d.assigned_to = None
            d.return_home()
        self.dice.clear()

    def draw(self, surface):
        r = self.rect
        pygame.draw.rect(surface, config.SLOT_BG, r, border_radius=10)
        pygame.draw.rect(surface, self.color, r, 3, border_radius=10)
        if not self.dice:
            icon = _icon(self.kind)
            if icon is not None:
                surface.blit(icon, (r.centerx - config.SLOT_ICON // 2, r.centery - config.SLOT_ICON // 2 - 4))
        font = pygame.font.SysFont('Arial', 16, bold=True)
        label = {'attack': 'ATTAQUE', 'defense': 'DÉFENSE', 'heal': 'SOIN'}[self.kind]
        t = font.render(label, True, self.color)
        surface.blit(t, (r.centerx - t.get_width() // 2, r.bottom + 4))
        if self.dice:
            big = pygame.font.SysFont('Arial', 34, bold=True)
            tot = big.render(f'{self.total}', True, self.color)
            surface.blit(tot, (r.centerx - tot.get_width() // 2, r.bottom + 24))

def make_slots():
    total_w = 3 * config.SLOT_W + 2 * config.SLOT_GAP
    x0 = (config.WIDTH - total_w) // 2
    kinds = ['attack', 'defense', 'heal']
    return [Slot(x0 + i * (config.SLOT_W + config.SLOT_GAP), config.SLOT_Y, k) for i, k in enumerate(kinds)]
