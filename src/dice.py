import random
import pygame
import config
import assets_loader
_cache = {}

def _sprite(faces, value):
    key = (faces, value)
    if key not in _cache:
        _cache[key] = assets_loader.load_image(f'dice/d{faces}_{value}.png', size=(config.DICE_SIZE, config.DICE_SIZE))
    return _cache[key]

class Die:

    def __init__(self, x, y, faces=6, value=1):
        self.x = x
        self.y = y
        self.size = config.DICE_SIZE
        self.faces = faces
        self.value = value

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def roll(self):
        self.value = random.randint(1, self.faces)

    def draw(self, surface):
        img = _sprite(self.faces, self.value)
        if img is None:
            return
        surface.blit(img, (self.x, self.y))

def make_row(count=None, faces=None):
    count = count or config.DICE_COUNT_DEFAULT
    faces = faces or config.DICE_FACES_DEFAULT
    total_w = count * config.DICE_SIZE + (count - 1) * config.DICE_GAP
    x0 = (config.WIDTH - total_w) // 2
    return [Die(x0 + i * (config.DICE_SIZE + config.DICE_GAP), config.DICE_TRAY_Y, faces=faces, value=1) for i in range(count)]
