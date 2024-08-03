import numpy as np
import pygame as pg


class Paddle:
    def __init__(self, xy: tuple):
        self.reset(xy)
        self.width = 20
        self.height = 100
    
    def reset(self, xy: tuple):
        self.xy = np.array(xy)
        self.vel = np.zeros(2, np.float32)
        self.angle = 0

    def update(self, dt: float):
        mpos = pg.mouse.get_pos()
        self.vel = (np.array(mpos) - self.xy) / dt
        self.xy = np.array(mpos)
    
    def render(self, display: pg.Surface):
        rect = pg.Rect(0, 0, self.width, self.height)
        rect.center = self.xy.astype(float)
        pg.draw.rect(display, (255, 0, 0), rect)