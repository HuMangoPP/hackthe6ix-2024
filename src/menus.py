import pygame as pg
import numpy as np
from .pyfont import *


class Menu:
    def __init__(self, screen_size: tuple, font: Font):
        self.screen_size = screen_size
        self.font = font

    def load(self):
        pass
    
    def update(self, dt: float, events: list[pg.Event]):
        pass

    def render(self, display: pg.Surface):
        pass


class StartMenu(Menu):
    def __init__(self, screen_size: tuple, font: Font):
        super().__init__(screen_size, font)
        self.start_button = pg.Rect(0, 0, screen_size[0] / 4, screen_size[1] / 8)
        self.start_button.center = (screen_size[0] / 2, screen_size[1] / 2)

        self.exit_button = pg.Rect(0, 0, screen_size[0] / 4, screen_size[1] / 8)
        self.exit_button.center = (screen_size[0] / 2, screen_size[1] / 2 + screen_size[1] / 6)

    def update(self, dt: float, events: list[pg.Event]):
        menu_return = dict(
            new_menu=None,
            exit=False
        )
        for event in events:
            if event.type == pg.MOUSEBUTTONUP:
                if self.start_button.collidepoint(event.pos):
                    menu_return['new_menu'] = 'game'
                if self.exit_button.collidepoint(event.pos):
                    menu_return['exit'] = True
        
        return menu_return
    
    def render(self, display: pg.Surface):
        pg.draw.rect(display, (255, 0, 0), self.start_button)
        self.font.render(
            display, 
            'start', 
            self.start_button.centerx, 
            self.start_button.centery, 
            (255, 255, 255), 
            self.screen_size[1] / 32,
            style='center'
        )

        pg.draw.rect(display, (255, 0, 0), self.exit_button)
        self.font.render(
            display, 
            'end', 
            self.exit_button.centerx, 
            self.exit_button.centery, 
            (255, 255, 255), 
            self.screen_size[1] / 32,
            style='center'
        )



class GameMenu(Menu):
    def __init__(self, screen_size: tuple, font: Font):
        super().__init__(screen_size, font)
        # from .paddle import ...
        # from .ball import ...
        # from .goal import ...
        self.timer = 5
    
    def load(self):
        self.timer = 5

    def update(self, dt: float, events: list[pg.Event]):
        menu_return = dict(
            new_menu=None,
            exit=False
        )
        self.timer -= dt
        if self.timer <= 0:
            menu_return['new_menu'] = 'end'

        return menu_return
    
    def render(self, display: pg.Surface):
        self.font.render(
            display,
            f'{int(np.ceil(self.timer))}',
            self.screen_size[0] / 2,
            self.screen_size[1] / 2,
            (255, 255, 255),
            self.screen_size[1] / 16,
            style='center'
        )


class EndMenu(Menu):
    def __init__(self, screen_size: tuple, font: Font):
        super().__init__(screen_size, font)
        self.play_again_button = pg.Rect(0, 0, screen_size[0] / 4, screen_size[1] / 8)
        self.play_again_button.center = (screen_size[0] / 2, screen_size[1] / 2)

        self.goto_main_button = pg.Rect(0, 0, screen_size[0] / 4, screen_size[1] / 8)
        self.goto_main_button.center = (screen_size[0] / 2, screen_size[1] / 2 + screen_size[1] / 6)
    
    def update(self, dt: float, events: list[pg.Event]):
        menu_return = dict(
            new_menu=None,
            exit=False
        )
        for event in events:
            if event.type == pg.MOUSEBUTTONUP:
                if self.play_again_button.collidepoint(event.pos):
                    menu_return['new_menu'] = 'game'
                if self.goto_main_button.collidepoint(event.pos):
                    menu_return['new_menu'] = 'start'
        
        return menu_return
    
    def render(self, display: pg.Surface):
        pg.draw.rect(display, (255, 0, 0), self.play_again_button)
        self.font.render(
            display, 
            'play again', 
            self.play_again_button.centerx, 
            self.play_again_button.centery, 
            (255, 255, 255), 
            self.screen_size[1] / 32,
            style='center'
        )

        pg.draw.rect(display, (255, 0, 0), self.goto_main_button)
        self.font.render(
            display, 
            'main menu', 
            self.goto_main_button.centerx, 
            self.goto_main_button.centery, 
            (255, 255, 255), 
            self.screen_size[1] / 32,
            style='center'
        )
