#!/usr/bin/env python
import pygame as pg


def main():
    pg.init()
    display = pg.display.set_mode((1280, 720))
    clock = pg.time.Clock()
    
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

        display.fill((67, 85, 125))
        pg.display.flip()

        pg.display.set_caption(f'fps: {clock.get_fps()}')

    pg.quit()


if __name__ == '__main__':
    main()