import numpy as np
import pygame as pg
import math

class Paddle:
    def __init__(self, center: tuple = (0,0), height: float = 60, width: float = 15, sprite_path: str = ""):
        self.vel = np.zeros(2, np.float32)
        self.ang_vel = np.zeros(2, np.float32)
        self.center = np.array(center, np.float32)

        self.colour = (255, 0, 0)
        self.width = width
        self.height = height
        self.corners = {
            "top_left": np.array([center[0] - width / 2, center[1] - height / 2]),
            "top_right": np.array([center[0] + width / 2, center[1] - height / 2]),
            "bot_left": np.array([center[0] - width / 2, center[1] + height / 2]),
            "bot_right": np.array([center[0] + width / 2, center[1] + height / 2])
        }

        if (sprite_path == ""):
            self.sprite = None
        else:
            self.sprite = pg.transform.smoothscale(pg.image.load(sprite_path), (self.width, self.height))
        
    """
    new_box is a tuple of 4 tuples arranged such that:
        new_box[0] is the top left corner of the paddle
        new_box[1] is the top right corner of the paddle
        new_box[2] is the bottom left corner of the paddle
        new_box[3] is the bottom right corner of the paddle
    """
    def update(self, dt: float, new_box: tuple):
        top_left = np.array(new_box[0])
        top_right = np.array(new_box[1])
        bot_left = np.array(new_box[2])
        bot_right = np.array(new_box[3])
        center = (top_left + bot_right) / 2

        # compute rotation angle
        original_vec = self.corners["top_left"] - self.center
        new_vec = top_left - center
        angle = math.atan2(original_vec[1], original_vec[0]) - math.atan2(new_vec[1], new_vec[0])
        self.ang_vel = angle / dt

        self.corners["top_left"] = top_left
        self.corners["top_right"] = top_right
        self.corners["bot_left"] = bot_left
        self.corners["bot_right"] = bot_right

        self.vel = (center - self.center) / dt
        self.center = center
    
    def compute_transferred_velocity(self, point_of_collision: tuple, xoffset: float, yoffset: float):
        tangent_vel = self.ang_vel * np.linalg.norm(self.center - np.array(point_of_collision)) * np.sign(np.array([xoffset, yoffset]))

        return tangent_vel + self.vel

    def render(self, display: pg.Surface):
        paddle = pg.Rect(self.corners.top_left[0], self.corners.top_left[1], self.width, self.height)
        paddle.topleft = self.corners.top_left
        paddle.topright = self.corners.top_right
        paddle.bottomleft = self.corners.bot_left
        paddle.bottomright = self.corners.bot_right
        if (self.sprite is not None):
            pg.draw.rect(display, self.colour, paddle)
        else:
            display.blit(self.sprite, paddle)

