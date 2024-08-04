import numpy as np
import pygame as pg
from .paddle import Paddle
from .goal import Goal


class Ball:
    def __init__(self, screen_size: tuple, sprite_path: str = '', speed_mult: float = 0.9):
        self.screen_size = screen_size
        self.reset()

        self.speed_mult = speed_mult
        self.colour = (0, 0, 255)
        self.size = 20

        self.iframes = [0, 0]

        if sprite_path:
            sprite = pg.image.load(sprite_path).convert()
            sprite.set_colorkey((255, 0, 0))
            self.sprite = pg.transform.scale_by(sprite, self.size * 2 / sprite.get_width())
        else:
            self.sprite = None
        
        self.honk = pg.mixer.Sound('./assets/honk.mp3')
    
    def reset(self):
        self.xy = np.array(self.screen_size) / 2 - np.array([100, 0])
        self.prev_xy = self.xy.copy()
        self.vel = np.array([0, 0])

        self.iframes = [0, 0]

    def _check_collide_wall(self):
        if self.xy[0] <= self.size:
            self.vel[0] = np.abs(self.vel[0]) * self.speed_mult
            self.xy[0] = self.size
        elif self.xy[0] >= self.screen_size[0] - self.size:
            self.vel[0] = -np.abs(self.vel[0]) * self.speed_mult
            self.xy[0] = self.screen_size[0] - self.size

        if self.xy[1] <= self.size:
            self.vel[1] = np.abs(self.vel[1]) * self.speed_mult
            self.xy[1] = self.size
        elif self.xy[1] >= self.screen_size[1] - self.size:
            self.vel[1] = -np.abs(self.vel[1]) * self.speed_mult
            self.xy[1] = self.screen_size[1] - self.size

    def check_collide_paddle(self, paddle: Paddle):
        if self.iframes[paddle.side] > 0:
            self.iframes[paddle.side] -= 1
            return 

        rotation = np.array([
            [np.cos(paddle.angle), -np.sin(paddle.angle)],
            [np.sin(paddle.angle), np.cos(paddle.angle)]
        ])
        prev_paddle_xy = np.dot(rotation, paddle.prev_xy)
        paddle_xy = np.dot(rotation, paddle.xy)
        paddle_vel = np.dot(rotation, paddle.vel)

        prev_ball_xy = np.dot(rotation, self.prev_xy)
        ball_xy = np.dot(rotation, self.xy)
        ball_vel = np.dot(rotation, self.vel)

        prev_xoffset = prev_ball_xy[0] - prev_paddle_xy[0]
        xoffset = ball_xy[0] - paddle_xy[0]
        prev_yoffset = prev_ball_xy[1] - prev_paddle_xy[1]
        yoffset = ball_xy[1] - paddle_xy[1]
        collide = False
        if (
            np.sign(prev_xoffset) != np.sign(xoffset) and
            (
                min(np.abs(prev_yoffset), np.abs(yoffset)) <= paddle.height / 2 or
                np.sign(prev_yoffset) != np.sign(yoffset)
            )
        ):
            collide = True
            ball_vel[0] = -ball_vel[0]
        
        if (
            np.sign(prev_yoffset) != np.sign(yoffset) and
            (
                min(np.abs(prev_xoffset), np.abs(xoffset)) <= paddle.width / 2 or
                np.sign(prev_xoffset) != np.sign(xoffset)
            )
        ):
            collide = True
            ball_vel[1] = -ball_vel[1]
        
        if collide:
            ball_vel = ball_vel * self.speed_mult + paddle_vel * self.speed_mult
            self.iframes[paddle.side] = 5
            self.honk.play()
            
            
            inv_rotation = np.array([
                [np.cos(-paddle.angle), -np.sin(-paddle.angle)],
                [np.sin(-paddle.angle), np.cos(-paddle.angle)]
            ])
            self.vel = np.dot(inv_rotation, ball_vel)
            self.xy = np.dot(inv_rotation, prev_ball_xy)
        
        spd = np.linalg.norm(self.vel)
        if spd > 0:
            self.vel = self.vel / spd * np.clip(spd, a_min=100, a_max=1000)

    def check_collide_goal(self, goal: Goal):
        if goal.rect.collidepoint(self.xy):
            self.reset()
            return True
        return False

    def update(self, dt: float):
        self.prev_xy = self.xy.copy()
        self.xy = self.prev_xy + dt * self.vel
        self._check_collide_wall()
    
    def render(self, display: pg.Surface):
        if self.sprite is not None:
            rect = self.sprite.get_rect()
            rect.center = self.xy
            display.blit(self.sprite, rect)
        else:
            pg.draw.circle(display, self.colour, self.xy.astype(float), self.size)

    