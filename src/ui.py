import pygame
import config

class Button:

    def __init__(self, rect, label, on_click=None):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.on_click = on_click
        self.enabled = True
        self._font = pygame.font.SysFont('Arial', 26, bold=True)

    def handle(self, event):
        if not self.enabled:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()
                return True
        return False

    def draw(self, surface):
        mx, my = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mx, my)
        if not self.enabled:
            color = config.BTN_DISABLED
        else:
            color = config.BTN_BG_HOVER if hover else config.BTN_BG
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, config.BTN_BORDER, self.rect, 2, border_radius=8)
        t = self._font.render(self.label, True, config.BTN_BORDER)
        surface.blit(t, (self.rect.centerx - t.get_width() // 2, self.rect.centery - t.get_height() // 2))
