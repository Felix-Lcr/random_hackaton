import config
import assets_loader
import hp_bar

class Hero:

    def __init__(self):
        self.x = config.HERO_X
        self.y = config.HERO_Y
        self.hp = config.HERO_MAX_HP
        self.max_hp = config.HERO_MAX_HP
        self.block = 0
        self.sprite = assets_loader.load_image('hero.png', size=(config.HERO_W, config.HERO_H))

    def draw(self, surface):
        if self.sprite is not None:
            surface.blit(self.sprite, (self.x - config.HERO_W // 2, self.y - config.HERO_H))
        hp_bar.draw(surface, self.x, self.y - config.HERO_H - 20, self.hp, self.max_hp, label='HÉROS')
