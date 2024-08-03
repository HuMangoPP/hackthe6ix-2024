import numpy as np
import pygame as pg

class Goal:
  # type 0 = garbage, type 1 = recycling, type 2 = organics
  def __init__(self, center:tuple = (0,0), type:int = 0, height:float = 150, sprite_path:str = ""):
    self.center = np.array(center, np.float32)
    self.height = height
    self.type = type

    if (sprite_path == ""):
      self.sprite = None
    else :
      self.sprite = pg.transform.smoothscale(pg.image.load(sprite_path), (50, height))
  
  def render(self, display: pg.Surface):
    if (self.sprite is None):
      goal = pg.Rect(self.center[0], self.center[1], 50, self.height)
      pg.draw.rect(display, (255, 255, 255), goal)
    else:
      display.blit(self.sprite, self.center)


