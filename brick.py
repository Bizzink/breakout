import pygame as pg

screen = None


def init(window, row_strengths, cols, s_width, brick_height):
    """row_strengths is an array of brick strengths per row, amount of rows = len(row_strengths)"""
    global screen
    screen = window

    bricks = []

    for row, strength in enumerate(row_strengths):
        for col in range(cols):
            if strength > 0:
                new_brick = Brick(col * s_width // cols, row * brick_height, s_width // cols, brick_height, strength)
                bricks.append(new_brick)

    return bricks


class Brick:
    def __init__(self, x, y, w, h, strength):
        self.rect = pg.Rect(x, y, w, h)
        self.strength = strength

        if self.strength > 6:
            self.strength = 6

        if self.strength < 1:
            self.strength = 1

    def __str__(self):
        return str(self.rect.topleft) + "\t" + str(self.strength)

    def draw(self):
        pg.draw.rect(screen, (0, 0, 0), self.rect)
        pg.draw.rect(screen, (255 // self.strength, 255 - (255 // self.strength), 255), (self.rect[0] + 1, self.rect[1] + 1, self.rect[2] - 2, self.rect[3] - 2))

    def hit(self):
        """action if ball hits brick"""
        self.strength -= 1

        if self.strength == 0:
            return True

        return False
