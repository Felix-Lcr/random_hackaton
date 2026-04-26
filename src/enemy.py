import random
import config
import assets_loader
import hp_bar
ENEMY_NAMES = ['Gobelin', 'Orc', 'Squelette', 'Troll']

class Enemy:

    def __init__(self, level=1):
        self.x = config.ENEMY_X
        self.y = config.ENEMY_Y
        self.max_hp = config.ENEMY_MAX_HP + (level - 1) * 6
        self.hp = self.max_hp
        self.name = ENEMY_NAMES[(level - 1) % len(ENEMY_NAMES)]
        self.dice_count = config.ENEMY_DICE_COUNT + (level - 1) // 2
        self.dice_faces = config.ENEMY_DICE_FACES
        self.last_roll = []
        self.level = level
        self.sprite = assets_loader.load_image('enemy.png', size=(config.ENEMY_W, config.ENEMY_H))

    def roll_attack(self):
        self.last_roll = [random.randint(1, self.dice_faces) for _ in range(self.dice_count)]
        return sum(self.last_roll)

    def draw(self, surface):
        if self.sprite is not None:
            surface.blit(self.sprite, (self.x - config.ENEMY_W // 2, self.y - config.ENEMY_H))
        hp_bar.draw(surface, self.x, self.y - config.ENEMY_H - 20, self.hp, self.max_hp, label=self.name)
