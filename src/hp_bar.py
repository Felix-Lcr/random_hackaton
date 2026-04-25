import pygame
import config
_font = None

def _get_font():
    global _font
    if _font is None:
        _font = pygame.font.SysFont('Arial', 16, bold=True)
    return _font

def draw(surface, cx, top_y, hp, max_hp, label=None, width=140):
    rect = pygame.Rect(cx - width // 2, top_y, width, 14)
    pygame.draw.rect(surface, config.HP_BAR_BG, rect, border_radius=4)
    ratio = max(0.0, hp / max_hp) if max_hp else 0
    if ratio > 0:
        fill = rect.copy()
        fill.width = int(rect.width * ratio)
        pygame.draw.rect(surface, config.HP_BAR_RED, fill, border_radius=4)
    pygame.draw.rect(surface, config.HP_BAR_BORDER, rect, 2, border_radius=4)
    txt = _get_font().render(f'{hp} / {max_hp}', True, config.WHITE)
    surface.blit(txt, (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2))
    if label:
        lbl = _get_font().render(label, True, config.WHITE)
        surface.blit(lbl, (rect.centerx - lbl.get_width() // 2, rect.top - 20))
