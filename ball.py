from math import pi, sin, cos
from random import randrange
import pygame as pg


screen = None
width, height = 0, 0


def init(window, ball_size, s_width, s_height):
    global screen, width, height
    screen = window
    width, height = s_width, s_height

    new_paddle = Paddle(s_height - (s_height // 8), s_width // 6, s_height // 40, s_width // 2)
    new_ball = Ball(ball_size, s_width // 2, new_paddle.rect.top - (ball_size // 2))

    return new_ball, new_paddle


class Ball:
    def __init__(self, size, x, y):
        self.rect = pg.Rect(0, 0, size, size)
        self.rect.center = (x, y)
        self.pos = [x, y]

        self.angle = randrange(35, 55)

        if randrange(20) > 10:
            self.angle *= -1

        self.angle -= 90

        self.angle *= pi/180

    def __str__(self):
        return str(self.rect.center) + "\t" + str(self.rect.width)

    def draw(self):
        pg.draw.ellipse(screen, (255, 255, 255), self.rect)

    def bounce_rect(self, rect):
        """finds the closest side of a rect, to determine which side it hit (and bounce off)
        side names are with respect to self, not rect"""

        top_dist = abs(self.rect.top - rect.bottom)
        bottom_dist = abs(self.rect.bottom - rect.top)
        left_dist = abs(self.rect.left - rect.right)
        right_dist = abs(self.rect.right - rect.left)

        closest = min(top_dist, bottom_dist, left_dist, right_dist)

        if closest == top_dist:
            self.angle = abs(self.angle)
            self.pos[1] = rect.bottom + self.rect.width // 2 + 1

        if closest == bottom_dist:
            self.angle = abs(self.angle) * -1
            self.pos[1] = rect.top - self.rect.width // 2 - 1

        if closest == left_dist:
            self.angle -= (self.angle - (pi / 2)) * 2
            self.pos[0] = rect.right + self.rect.width // 2 + 1

        if closest == right_dist:
            self.angle -= (self.angle - (pi / 2)) * 2
            self.pos[0] = rect.left - self.rect.width // 2 - 1

    def move(self, dist):
        """move the ball and change direction if it hits a wall"""
        self.pos[0] += cos(self.angle) * dist
        self.pos[1] += sin(self.angle) * dist

        self.rect.center = self.pos

        #  Ball hit left side
        if self.rect.left < 0:
            self.rect.left = 1
            self.pos[0] = self.rect.centerx
            self.angle -= (self.angle - (pi / 2)) * 2

        #  Ball hit right side
        if self.rect.right > width:
            self.rect.right = width - 1
            self.pos[0] = self.rect.centerx
            self.angle -= (self.angle - (pi / 2)) * 2

        #  Ball hit top
        if self.rect.top < 0:
            self.rect.top = 1
            self.angle *= -1
            self.pos[1] = self.rect.centery

        #  Keep angle within -pi - pi
        while self.angle > pi:
            self.angle -= pi * 2

        while self.angle < -pi:
            self.angle += pi * 2


class Paddle:
    def __init__(self, pos, w, h, center):
        self.rect = pg.Rect(0, 0, w, h)
        self.rect.centery = pos
        self.pos = center  # Good names
        self.moving = None

    def draw(self):
        self.rect.centerx = int(self.pos)
        pg.draw.rect(screen, (150, 150, 150), self.rect)

    def move(self, dist):
        """move paddle, if it his a wall, don't move"""
        self.pos += dist
        self.moving = dist

        if self.pos < self.rect.width / 2:
            self.pos = self.rect.width / 2
            self.moving = None

        if self.pos > width - (self.rect.width / 2):
            self.pos = width - (self.rect.width / 2)
            self.moving = None
