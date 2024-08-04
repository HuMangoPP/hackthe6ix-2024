#!/usr/bin/env python
import pygame as pg
import mediapipe as mp
import cv2 as cv
from src import *

def main():
    pg.init()
    pg.mixer.init()
    screen_size = (1920, 1080)
    display = pg.display.set_mode(screen_size)
    clock = pg.time.Clock()
    font = Font(pg.image.load('./src/pyfont/font.png').convert())
    
    capture = cv.VideoCapture(0)
    mp_face_detection = mp.solutions.face_detection

    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=1) as face_detection:
        menus = dict(
            start=StartMenu(screen_size, font),
            game=GameMenu(screen_size, font, capture, face_detection),
            settings=SettingsMenu(screen_size, font),
            end=EndMenu(screen_size, font)
        )
        current_menu = 'start'

        osts = dict(
            idle=pg.mixer.Sound('./assets/menu_theme.mp3'),
            battle=pg.mixer.Sound('./assets/battle_theme.mp3')
        )
        osts['battle'].set_volume(0.5)
        osts['idle'].set_volume(0.5)
        osts['idle'].play(-1, fade_ms=1000)
        running = True
        while running:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    running = False
            
            dt = clock.get_time() / 1000
            clock.tick(60)
            menu_return = menus[current_menu].update(dt, events)
            if menu_return['exit']:
                running = False
            if menu_return['new_menu']:
                current_menu = menu_return['new_menu']
                menus[current_menu].load(menu_return)

                if current_menu == 'game':
                    osts['idle'].stop()
                    osts['battle'].play(-1, fade_ms=1000)
                if current_menu == 'start':
                    osts['battle'].stop()
                    osts['idle'].play(-1, fade_ms=1000)
            if 'mute' in menu_return:
                if osts['idle'].get_volume() > 0:
                    osts['idle'].set_volume(0)
                    osts['battle'].set_volume(0)
                else:
                    osts['idle'].set_volume(0.5)
                    osts['battle'].set_volume(0.5)

            display.fill((90, 120, 200))
            menus[current_menu].render(display)
            pg.display.flip()

            pg.display.set_caption(f'fps: {clock.get_fps()}')

    pg.quit()


if __name__ == '__main__':
    main()