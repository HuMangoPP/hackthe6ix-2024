import numpy as np
import pygame as pg

class Goal:
    # type 0 = garbage, type 1 = recycling, type 2 = organics
    def __init__(self, screen_size: tuple, type: int = 0, height: float = 150, sprite_path: str = ""):
        self.center = np.array(screen_size) * np.array([1, 1/2])
        self.height = height
        self.type = type

        if (sprite_path == ""):
            self.sprite = None
            self.rect = pg.Rect(0, 0, 50, height)
            self.rect.center = self.center.astype(float)
        else :
            self.sprite = pg.image.load(sprite_path).convert()
            self.sprite = pg.transform.scale_by(self.sprite, height / self.sprite.get_height())
            self.rect = self.sprite.get_rect()
            self.rect.center = self.center.astype(float)
    
    def render(self, display: pg.Surface):
        if (self.sprite is None):
            pg.draw.rect(display, (255, 255, 255), self.rect)
        else:
            display.blit(self.sprite, self.rect)


