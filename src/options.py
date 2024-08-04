import pygame as pg
from .pyfont import *


class Options:
  def __init__(self, screen_size: tuple, y: float, text: str, options: dict, font: Font, font_size:float =20, settings_data: list[dict] | None = None):
    self.section = pg.Rect(0, 0, screen_size[0] / 3, screen_size[1] / 6)
    self.section.center = (screen_size[0] / 2, y)
    self.text = text
    self.options = settings_data
    if (settings_data is None):
      self.options = []
      for i, option in enumerate(options.keys()):
        self.options.append({
          "text": option,
          "value": options[option],
          "radio": (self.section.centerx + (i-1) * (self.section.width) / 3.5,
                    self.section.y + self.section.height * 0.65, 10),
          "selected": False
        }) 
    else:
      for i, option in enumerate(self.options):
        option["radio"] = (self.section.centerx + (i-1) * (self.section.width) / 3.5,
                    self.section.y + self.section.height * 0.65, 10)
    self.font = font
    self.font_size = font_size
    
  def update(self, event: pg.Event):    
    for i, option in enumerate(self.options):
      delta_x = event.pos[0] - option["radio"][0]
      delta_y = event.pos[1] - option["radio"][1]

      if (delta_x**2 + delta_y**2 <= option["radio"][2]**2):
        option["selected"] = True
        for j, option in enumerate(self.options):
          if (i != j):
            option["selected"] = False
        break

    
    return list(filter(lambda option: option["selected"], self.options))[0]
  
  def render(self, display: pg.Surface):
    pg.draw.rect(display, (255, 0, 0), self.section)
    self.font.render(
      display,
      self.text,
      self.section.topleft[0] + 35,
      self.section.topleft[1] + 35,
      (255, 255, 255),
      self.font_size,
      style='left'
    )

    for option in self.options:
      self.font.render(
        display,
        option["text"],
        option["radio"][0]+25,
        option["radio"][1],
        (255, 255, 255),
        self.font_size * 0.5,
        style='left'
      )
      pg.draw.circle(display, (255, 255, 255), (option["radio"][0], option["radio"][1]), option["radio"][2])
      if (option["selected"]):
        pg.draw.circle(display, (0, 0 , 0), (option["radio"][0], option["radio"][1]), option["radio"][2]*0.7)
    