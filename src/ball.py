import numpy as np
import pygame as pg
from .paddle import Paddle
from .goal import Goal


class Ball:
    def __init__(self, screen_size: tuple):
        self.screen_size = screen_size
        self.reset()

        self.colour = (255, 255, 255)
        self.size = 10
    
    def reset(self):
        self.xy = np.array(self.screen_size) / 2
        self.vel = np.zeros(2, np.float32)

    def _check_collide_wall(self):
        if self.xy[0] <= self.size:
            self.vel[0] = np.abs(self.vel[0])
            self.xy[0] = self.size
        elif self.xy[0] >= self.screen_size[0] - self.size:
            self.vel[0] = -np.abs(self.vel[0])
            self.xy[0] = self.screen_size[0] - self.size

        if self.xy[1] <= self.size:
            self.vel[1] = np.abs(self.vel[1])
            self.xy[1] = self.size
        elif self.xy[1] >= self.screen_size[1] - self.size:
            self.vel[1] = -np.abs(self.vel[1])
            self.xy[1] = self.screen_size[1] - self.size

    def check_collide_paddle(self, paddle: Paddle):
        rotation = np.array([
            [np.cos(paddle.angle), -np.sin(paddle.angle)],
            [np.sin(paddle.angle), np.cos(paddle.angle)]
        ])
        paddle_xy = np.dot(rotation, paddle.xy)
        ball_xy = np.dot(rotation, self.xy)

        if np.abs(ball_xy[0] - paddle_xy[0]) <= paddle.width / 2:
            xoffset = 0
        elif ball_xy[0] < paddle_xy[0]:
            xoffset = ball_xy[0] - (paddle_xy[0] - paddle.width / 2)
        else:
            xoffset = ball_xy[0] - (paddle_xy[0] + paddle.width / 2)
        
        if np.abs(ball_xy[1] - paddle_xy[1]) <= paddle.height / 2:
            yoffset = 0
        elif ball_xy[1] < paddle_xy[1]:
            yoffset = ball_xy[1] - (paddle_xy[1] - paddle.height / 2)
        else:
            yoffset = ball_xy[1] - (paddle_xy[1] + paddle.height / 2)
        
        if xoffset ** 2 + yoffset ** 2 <= self.size ** 2:
            ball_vel = np.dot(rotation, self.vel)
            paddle_disp = np.dot(rotation, paddle.vel)
            ball_spd = np.linalg.norm(ball_vel)
            if xoffset != 0:
                ball_vel[0] = ball_spd * np.sign(xoffset)
            if yoffset != 0:
                ball_vel[1] = ball_spd * np.sign(yoffset)
            ball_vel = ball_vel + paddle_disp

            if xoffset != 0 or yoffset != 0:
                ball_xy = ball_xy - np.array([xoffset, yoffset]) + self.size * np.array([xoffset, yoffset]) / np.linalg.norm([xoffset, yoffset])
            
            inv_rotation = np.array([
                [np.cos(-paddle.angle), -np.sin(-paddle.angle)],
                [np.sin(-paddle.angle), np.cos(-paddle.angle)]
            ])
            self.xy = np.dot(inv_rotation, ball_xy)
            self.vel = np.dot(inv_rotation, ball_vel)


    def check_collide_goal(self, goal: Goal):
        if goal.rect.collidepoint(self.xy):
            self.reset()
            return True
        return False


    def update(self, dt: float):
        self.xy = self.xy + dt * self.vel
        self._check_collide_wall()
    
    def render(self, display: pg.Surface):
        pg.draw.circle(display, self.colour, self.xy.astype(float), self.size)

    