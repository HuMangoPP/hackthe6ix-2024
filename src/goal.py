import numpy as np
import pygame as pg

class Goal:
    # type 0 = garbage, type 1 = recycling, type 2 = organics
    def __init__(self, xy: tuple, type: int = 0, height: float = 200, sprite_path: str = ""):
        self.xy = np.array(xy)
        self.height = height
        self.type = type

        if (sprite_path == ""):
            self.sprite = None
            self.rect = pg.Rect(0, 0, 200, height)
            self.rect.center = self.xy.astype(float)
        else:
            self.sprite = pg.image.load(sprite_path).convert()
            self.sprite.set_colorkey((255, 0, 0))
            if xy[0] < 960:
                self.sprite = pg.transform.flip(self.sprite, True, False)
            self.sprite = pg.transform.scale_by(self.sprite, height / self.sprite.get_height())
            self.rect = self.sprite.get_rect()
            self.rect.center = self.xy.astype(float)
    
    def render(self, display: pg.Surface):
        if self.sprite is None:
            pg.draw.rect(display, (0, 0, 0), self.rect)
        else:
            display.blit(self.sprite, self.rect)
