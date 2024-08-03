import pygame as pg
import numpy as np
import cv2 as cv
import mediapipe as mp
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
        from .paddle import Paddle
        from .ball import Ball
        from .goal import Goal

        self.countdown = 3

        self.left_score = 0
        self.right_score = 0

        self.left_paddle = Paddle(center=screen_size * np.array([1/4, 1/2]))
        self.right_paddle = Paddle(center=screen_size * np.array([3/4, 1/2]))

        self.ball = Ball(screen_size)

        self.left_goal = Goal(screen_size * np.array([0, 1/2]))
        self.right_goal = Goal(screen_size * np.array([1, 1/2]))
        self.capture = cv.VideoCapture(0)
        self.model = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=1.0)

    def load(self):
        self.countdown = 3
        self.left_score = 0
        self.right_score = 0

        self.left_paddle.reset(self.screen_size * np.array([1/4, 1/2]))
        self.right_paddle.reset(self.screen_size * np.array([3/4, 1/2]))

        self.ball.reset()

    def update(self, dt: float, events: list[pg.Event]):
        menu_return = dict(
            new_menu=None,
            exit=False
        )
        if self.countdown > 0:
            self.countdown -= dt
        else:
            self.left_paddle.update(dt, self.capture, self.model)
            self.ball.update(dt)
    
            self.ball.check_collide_paddle(self.left_paddle)
            self.ball.check_collide_paddle(self.right_paddle)
            if self.ball.check_collide_goal(self.left_goal):
                self.right_score += 1
            if self.ball.check_collide_goal(self.right_goal):
                self.left_score += 1

        return menu_return
    
    def render(self, display: pg.Surface):
        if self.countdown > 0:
            self.font.render(
                display,
                str(int(np.ceil(self.countdown))),
                self.screen_size[0] / 2,
                self.screen_size[1] / 2,
                (255, 255, 255),
                self.screen_size[1] / 8,
                style='center'
            )
        else:
            self.font.render(
                display, 
                str(self.left_score),
                self.screen_size[0] / 16,
                self.screen_size[1] / 8,
                (255, 255, 255),
                self.screen_size[1] / 16,
                style='center'
            )
            self.font.render(
                display, 
                str(self.right_score),
                self.screen_size[0] * 15 / 16,
                self.screen_size[1] / 8,
                (255, 255, 255),
                self.screen_size[1] / 16,
                style='center'
            )
            self.left_paddle.render(display)
            self.right_paddle.render(display)
            self.ball.render(display)
            self.left_goal.render(display)
            self.right_goal.render(display)


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
