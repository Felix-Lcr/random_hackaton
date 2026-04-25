import config
import assets_loader

class Enemy:

    def __init__(self):
        self.x = config.ENEMY_X
        self.y = config.ENEMY_Y
        self.sprite = assets_loader.load_image('enemy.png', size=(config.ENEMY_W, config.ENEMY_H))

    def draw(self, surface):
        if self.sprite is None:
            return
        surface.blit(self.sprite, (self.x - config.ENEMY_W // 2, self.y - config.ENEMY_H))
