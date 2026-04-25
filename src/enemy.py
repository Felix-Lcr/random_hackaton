import config
import assets_loader
import hp_bar

class Enemy:

    def __init__(self):
        self.x = config.ENEMY_X
        self.y = config.ENEMY_Y
        self.hp = config.ENEMY_MAX_HP
        self.max_hp = config.ENEMY_MAX_HP
        self.name = 'Gobelin'
        self.sprite = assets_loader.load_image('enemy.png', size=(config.ENEMY_W, config.ENEMY_H))

    def draw(self, surface):
        if self.sprite is not None:
            surface.blit(self.sprite, (self.x - config.ENEMY_W // 2, self.y - config.ENEMY_H))
        hp_bar.draw(surface, self.x, self.y - config.ENEMY_H - 20, self.hp, self.max_hp, label=self.name)
