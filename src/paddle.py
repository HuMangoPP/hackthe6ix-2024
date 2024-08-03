import cv2 as cv
import pygame as pg
import numpy as np
import mediapipe as mp

class Paddle:
    def __init__(self, center: tuple = (0,0), height: float = 60, width: float = 15, sprite_path: str = ""):
        self.vel = np.zeros(2, np.float32)
        self.angle = 0
        self.ang_vel = np.zeros(2, np.float32)
        self.xy = np.array(center, np.float32)

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
    
    def reset(self, center: tuple):
        self.xy = np.array(center, np.float32)
        width = self.width
        height = self.height
        self.corners = {
            "top_left": np.array([center[0] - width / 2, center[1] - height / 2]),
            "top_right": np.array([center[0] + width / 2, center[1] - height / 2]),
            "bot_left": np.array([center[0] - width / 2, center[1] + height / 2]),
            "bot_right": np.array([center[0] + width / 2, center[1] + height / 2])
        }
        
    def find_closest_face(self, frame: np.array, face_detection):
        results = face_detection.process(frame)

        if (results.detections):
            distances = []
            for detection in results.detections:
                key_points = np.array([(p.x, p.y) for p in detection.location_data.relative_keypoints]) 
                key_points_coords = np.multiply(key_points,[1920,1080],).astype(int)
                eye_points = key_points_coords[0:2]
                midpoint = (eye_points[0] + eye_points[1]) / 2
                distances.append(np.linalg.norm(self.xy - midpoint))
            
            shortest_distance = min(distances)

            return results.detections[distances.index(shortest_distance)]

    def rotation_matrix(self, angle: float):
        return np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])

    def update(self, dt: float, capture: cv.VideoCapture, face_detection):
        ret, frame = capture.read()
        face = self.find_closest_face(frame, face_detection)
        if (face):
            eye_points = np.array([(p.x * 1920, p.y * 1080) for p in face.location_data.relative_keypoints][0:2])
            angle_from_horizontal = np.arctan2(eye_points[0][1] - eye_points[1][1], eye_points[0][0] - eye_points[1][0])
            midpoint = (eye_points[0] + eye_points[1]) / 2
            rotation_matrix = self.rotation_matrix(angle_from_horizontal)
            top_left = np.dot(rotation_matrix, np.array([midpoint[0] - self.width / 2, midpoint[1] - self.height / 2]))
            top_right = np.dot(rotation_matrix, np.array([midpoint[0] + self.width / 2, midpoint[1] - self.height / 2]))
            bot_left = np.dot(rotation_matrix, np.array([midpoint[0] - self.width / 2, midpoint[1] + self.height / 2]))
            bot_right = np.dot(rotation_matrix, np.array([midpoint[0] - self.width / 2, midpoint[1] + self.height / 2]))

            # compute rotation angle
            angle = angle_from_horizontal - self.angle
            self.ang_vel = angle / dt

            self.corners["top_left"] = top_left
            self.corners["top_right"] = top_right
            self.corners["bot_left"] = bot_left
            self.corners["bot_right"] = bot_right

            self.vel = (midpoint - self.xy) / dt
            self.xy = midpoint
            self.angle = angle_from_horizontal
    
    def compute_transferred_velocity(self, point_of_collision: tuple, xoffset: float, yoffset: float):
        tangent_vel = self.ang_vel * np.linalg.norm(self.xy - np.array(point_of_collision)) * np.sign(np.array([xoffset, yoffset]))

        return tangent_vel + self.vel

    def render(self, display: pg.Surface):
        paddle = pg.Rect(self.corners["top_left"][0], self.corners["top_left"][1], self.width, self.height)
        paddle.topleft = self.corners["top_left"]
        paddle.topright = self.corners["top_right"]
        paddle.bottomleft = self.corners["bot_left"]
        paddle.bottomright = self.corners["bot_right"]
        if (self.sprite is None):
            pg.draw.rect(display, self.colour, paddle)
        else:
            display.blit(self.sprite, paddle)
