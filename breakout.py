from random import randrange
import pygame as pg
from time import time
import brick as br
import ball as ba


def tick():
    """movement based on time difference so that framerate doesnt effect movement"""
    global prev_tick
    dist = time() - prev_tick

    if 276 in pressed_keys or 97 in pressed_keys:  # left arrow, A
        paddle.move(-dist * speed)

    if 275 in pressed_keys or 100 in pressed_keys:  # right arrow, D
        paddle.move(dist * speed)

    ball.move(dist * speed)
    prev_tick = time()


def reset():
    global bricks, ball, paddle
    bricks = br.init(screen, (0, 0, 0, 6, 5, 4, 3, 2, 1, 1), 10, width, 20)
    ball, paddle = ba.init(screen, 15, width, height)


def pause():
    global prev_tick
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == 27:
                    prev_tick = time()
                    return


width, height = 500, 500

pg.init()
screen = pg.display.set_mode((width, height))
bricks = br.init(screen, (0, 0, 0, 6, 5, 4, 3, 2, 1, 1), 10, width, 20)
ball, paddle = ba.init(screen, 15, width, height)

pressed_keys = []
prev_tick = time()
speed = 200

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

        if event.type == pg.KEYDOWN:
            pressed_keys.append(event.key)

        if event.type == pg.KEYUP:
            if event.key in pressed_keys:
                pressed_keys.remove(event.key)

    if 27 in pressed_keys:  # Esc
        pause()
        pressed_keys.remove(27)

    tick()

    for brick in bricks:
        if ball.rect.colliderect(brick.rect):
            destroy = brick.hit()
            ball.bounce_rect(brick.rect)
            if destroy:
                bricks.remove(brick)

    if ball.rect.colliderect(paddle.rect):
        ball.bounce_rect(paddle.rect)

        if paddle.moving is not None:
            ball.angle += paddle.moving * randrange(10) / 20

    if ball.rect.top > height:
        reset()

    paddle.moving = None

    screen.fill((0, 0, 0))

    for brick in bricks:
        brick.draw()

    ball.draw()
    paddle.draw()

    pg.display.flip()
