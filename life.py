"""
The following is just a demo of what this engine is capable of, in its infant state.
"""
import pygame
from pygame.locals import *
pygame.init()

import sys

from multiarray import ndimensional
from display import get_view, drawn_view, screenshot
from inputs import input_board
from utils import randomize2d
from automata import life2d
from frames import update_all, add_frame, draw_frame, update_frame, get_frame_at, get_frame_data, export_to_gif
import cubes

n = 3
d = 32
ax1, ax2, ax3= 0, 1, 2
pos = [0 for _ in range(n)]
PW = 3

cubes.add_cube("clear", 2, (d, d), 0)
cubes.add_cube("randomized", 2, (d, d), 0)
randomize2d(cubes.get_cube("randomized"))
cubes.add_cube("life", 2, (d, d), 0)
cubes.build_cube("life", "randomized", 60, life2d)


WIDTH, HEIGHT = 1400, 1000
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
HEL16 = pygame.font.SysFont("Condensed", 16)
CLOCK = pygame.time.Clock()

order = ["x", "y", "z", "a", "b", "c", "d", "e", "f", "g"]
mpos = (0, 0)
add_frame("split", (WIDTH//2, 0), (WIDTH//2, HEIGHT), PW, "life", "list", tuple(pos), ax1, ax2, ax3)
add_frame("show", (0, 0), (WIDTH//2, HEIGHT), PW*2, "life", "animation", tuple(pos), ax1, ax2, ax3)
while True:
    name = get_frame_at(mpos)
    if name is not None:
        data = get_frame_data(name)
        PW = data["pixelwidth"]
        ax1, ax2, ax3 = data["axis1"], data["axis2"], data["index"]
        pos = list(data["viewpos"])
    
    mods = pygame.key.get_mods()
    change = False
    bchange = False
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
                cubes.add_cube("randomized", 2, (d, d), 0)
                randomize2d(cubes.get_cube("randomized"))
                cubes.build_cube("life", "randomized", 60, life2d)
                bchange = True
                
            if e.key == K_c:
                cubes.build_cube("life", "clear", 60, life2d)
                bchange = True
                
            if e.key == K_RETURN:
                cube = input_board(SCREEN, (32, 32), (d, d), style='bool', startfrom=cubes.get_cube("life")[0])
                cubes.add_pre_built("user", (d, d), cube)
                cubes.build_cube("life", "user", 60, life2d)
                bchange = True
            change = True
                
        elif e.type == MOUSEMOTION:
            mpos = e.pos

    if bchange:
        update_all()
    elif change:
        if name is not None:
            update_frame(name, None, PW, tuple(pos), None, None, ax1, ax2, ax3)

    if gif and name is not None:
        export_to_gif(name)

    SCREEN.fill((100, 100, 100))
    
    draw_frame(SCREEN, "split", HEL16, (0, 0, 0) if name != "split" else (0, 200, 0))
    draw_frame(SCREEN, "show", HEL16, (0, 0, 0) if name != "show" else (0, 200, 0))
    pygame.display.update()
    CLOCK.tick(15)
