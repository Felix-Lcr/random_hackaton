import config
import assets_loader

class Hero:

    def __init__(self):
        self.x = config.HERO_X
        self.y = config.HERO_Y
        self.sprite = assets_loader.load_image('hero.png', size=(config.HERO_W, config.HERO_H))

    def draw(self, surface):
        if self.sprite is None:
            return
        surface.blit(self.sprite, (self.x - config.HERO_W // 2, self.y - config.HERO_H))
