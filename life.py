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
from frames import add_frame, draw_frame, update_frame, get_frame_at, get_frame_data, export_to_gif

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

WIDTH, HEIGHT = 1400, 1000
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
HEL16 = pygame.font.SysFont("Condensed", 16)
CLOCK = pygame.time.Clock()

order = ["x", "y", "z", "a", "b", "c", "d", "e", "f", "g"]
mpos = (0, 0)
add_frame("split", (WIDTH//2, 0), (WIDTH//2, HEIGHT), PW, cube, "animation", tuple(pos), ax1, ax2, ax3)
add_frame("show", (0, 0), (WIDTH//2, HEIGHT), PW*2, cube, "animation", tuple(pos), ax1, ax2, ax3)
while True:
    name = get_frame_at(mpos)
    if name is not None:
        data = get_frame_data(name)
        PW = data["pixelwidth"]
        ax1, ax2, ax3 = data["axis1"], data["axis2"], data["axis3"]
        pos = list(data["viewpos"])
    
    mods = pygame.key.get_mods()
    change = False
    cubechange = False
    gif=False
    for e in pygame.event.get():
        if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()

        if e.type == KEYDOWN and mods & KMOD_SHIFT:
            if e.key == K_RIGHT:
                ax1, ax2, ax3 = ax2, ax3, ax1
            if e.key == K_LEFT:
                ax1, ax2, ax3 = ax3, ax1, ax2
            if e.key == K_UP:
                ax1, ax2, ax3 = ax2, ax1, ax3
            if e.key == K_DOWN:
                ax1, ax2, ax3 = ax1, ax3, ax2
                
            change = True

        elif e.type == KEYDOWN:
            if e.key == K_PERIOD: screenshot(SCREEN)
            if e.key == K_COMMA: gif=True
            
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
                cubechange = True

            if e.key == K_c:
                cube = build(ndimensional(2, d, filler=0))
                cubechange = True

            if e.key == K_RETURN:
                cube = build(input_board(SCREEN, (32, 32), d, d, startfrom=cube[0]))
                cubechange = True

            change = True
                
        elif e.type == MOUSEMOTION:
            mpos = e.pos

    if change:
        if name is not None:
            update_frame(name, cube, PW, tuple(pos), None, None, ax1, ax2, ax3)

    if cubechange:
        update_frame("split", cube)
        update_frame("show", cube)

    if gif and name is not None:
        export_to_gif(name)

    SCREEN.fill((100, 100, 100))
    
    draw_frame(SCREEN, "split", HEL16, (0, 0, 0) if name != "split" else (0, 200, 0))
    draw_frame(SCREEN, "show", HEL16, (0, 0, 0) if name != "show" else (0, 200, 0))
    pygame.display.update()
    CLOCK.tick(15)
