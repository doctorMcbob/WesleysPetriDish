"""
The following is just a demo of what this engine is capable of, in its infant state.
"""
import pygame
from pygame.locals import *
pygame.init()

import sys

from multiarray import ndimensional
from display import get_view, drawn_view, screenshot, input_board
from utils import randomize2d
from automata import life2d
from frames import add_frame, draw_frame, update_frame

n = 3
d = 32
ax1, ax2, ax3= 0, 1, 2
pos = [0 for _ in range(n)]
PW = 3

def build(start):
    cube = []
    board = start
    while len(cube) < 60:
        cube.append(board)
        board = life2d(board)
    return cube
        
board = ndimensional(2, d, filler=0)
randomize2d(board)
cube = build(board)

WIDTH, HEIGHT = 1100, 876
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
HEL16 = pygame.font.SysFont("Helvetica", 16)

order = ["x", "y", "z", "a", "b", "c", "d", "e", "f", "g"]

add_frame("life", (0, 0), PW, cube, "list:1072,812", pos, ax1, ax2, ax3)
while True:
    mods = pygame.key.get_mods()
    change = False
    for e in pygame.event.get():
        if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()

        if e.type == KEYDOWN and mods & KMOD_SHIFT:
            if e.key == K_RIGHT: ax1 = min(n-1, ax1 + 1)
            if e.key == K_LEFT: ax1 = max(0, ax1 - 1)
            if e.key == K_UP: ax2 = min(n-1, ax2 + 1)
            if e.key == K_DOWN: ax2 = max(0, ax2 - 1)
            if e.key == K_w: ax3 = min(n-1, ax3 + 1)
            if e.key == K_s: ax3 = max(0, ax3 - 1)
            change = True

        elif e.type == KEYDOWN:
            if e.key == K_PERIOD: screenshot(SCREEN)
            
            if e.key == K_RIGHT: pos[0] -= 1
            if e.key == K_LEFT: pos[0] += 1
            if e.key == K_UP: pos[1] += 1
            if e.key == K_DOWN: pos[1] -= 1
            if e.key == K_w: pos[2] -= 1
            if e.key == K_s: pos[2] += 1

            if e.key == K_EQUALS:
                PW += 1
            if e.key == K_MINUS:
                PW = max(1, PW - 1)
            if e.key == K_r:
                board = ndimensional(2, d, filler=0)
                randomize2d(board)
                cube = build(board)

            if e.key == K_c:
                cube = build(ndimensional(2, d, filler=0))

            if e.key == K_RETURN:
                cube = build(input_board(SCREEN, (32, 32), d, d, startfrom=cube[0]))
            change = True

    if change:
        update_frame("life", cube, PW, pos, None, None, ax1, ax2, ax3)

    SCREEN.fill((100, 100, 100))
    draw_frame(SCREEN, "life", HEL16, (0, 0, 0))
    pygame.display.update()
