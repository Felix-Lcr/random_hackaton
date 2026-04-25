import pygame
import config
import assets_loader
_cache = [None, False]

def _image():
    if not _cache[1]:
        _cache[0] = assets_loader.load_image('arena.png', size=(config.WIDTH, config.HEIGHT))
        _cache[1] = True
    return _cache[0]

def draw(surface, t=0):
    surface.fill(config.BG)
    img = _image()
    if img is not None:
        surface.blit(img, (0, 0))
