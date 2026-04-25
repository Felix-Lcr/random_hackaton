import os
import pygame
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')

def load_image(name, size=None):
    path = os.path.join(ASSETS_DIR, name)
    if not os.path.isfile(path):
        return None
    try:
        img = pygame.image.load(path).convert_alpha()
        if size is not None:
            img = pygame.transform.smoothscale(img, size)
        return img
    except pygame.error:
        return None

def load_sound(name):
    path = os.path.join(ASSETS_DIR, name)
    if os.path.isfile(path):
        try:
            return pygame.mixer.Sound(path)
        except pygame.error:
            pass

    class _Silent:

        def play(self, *a, **kw):
            pass

        def stop(self, *a, **kw):
            pass

        def set_volume(self, *a, **kw):
            pass
    return _Silent()
