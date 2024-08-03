#!/usr/bin/env python
import pygame as pg
from src import *

def main():
    pg.init()
    screen_size = (1280, 720)
    display = pg.display.set_mode(screen_size)
    clock = pg.time.Clock()
    
    menus = dict(
        start=StartMenu(screen_size),
        game=GameMenu(screen_size)
    )
    current_menu = 'start'

    running = True
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
        
        dt = clock.get_time() / 1000
        clock.tick()
        menu_return = menus[current_menu].update(dt, events)
        if menu_return['exit']:
            running = False
        if menu_return['new_menu']:
            current_menu = menu_return['new_menu']

        display.fill((67, 85, 125))
        menus[current_menu].render(display)
        pg.display.flip()

        pg.display.set_caption(f'fps: {clock.get_fps()}')

    pg.quit()


if __name__ == '__main__':
    main()