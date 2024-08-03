import pygame as pg


class Menu:
    def __init__(self, screen_size: tuple):
        pass
    
    def update(self, dt: float, events: list[pg.Event]):
        pass

    def render(self, display: pg.Surface):
        pass


class StartMenu(Menu):
    def __init__(self, screen_size: tuple):
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
        pg.draw.rect(display, (255, 0, 0), self.exit_button)
