import pygame
from pygame.locals import *
pygame.init()

import sys

import frames
import cubes
import inputs
from automata import RULES

WIDTH, HEIGHT = 1200, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

FONTS = {
    "Helvetica": pygame.font.SysFont("Helvetica", 32),
    "Condensed": pygame.font.SysFont("Condensed", 32),
}
FONT = "Condensed"
CLOCK = pygame.time.Clock()

AXIS1 = None
AXIS2 = None
INDEX = None

PW = 4

MPOS = (0, 0)
RELATIVE_POSITION = None
CUBE = None

def process():
    global MPOS, FONT, AXIS1, AXIS2, INDEX, CUBE, RELATIVE_POSITION, PW
    name = frames.get_frame_at(MPOS)

    if name is not None:
        data = frames.get_frame_data(name)
        PW = data["pixelwidth"]
        AXIS1, AXIS2, INDEX = data["axis1"], data["axis2"], data["index"]
        RELATIVE_POSITION = list(data["viewpos"])

    mods = pygame.key.get_mods()
    board_changed = False
    view_changed = False
    
    gif = False
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()

        if e.type == KEYDOWN and mods & KMOD_CTRL:
            if e.key == K_ESCAPE:
                sys.exit()

            if e.key == K_s:
                inputs.input_save_frame(SCREEN, FONTS[FONT], SCREEN, draw)

            if e.key == K_o:
                inputs.input_load_frame(SCREEN, FONTS[FONT], SCREEN, draw)
            
        elif e.type == KEYDOWN and mods & KMOD_SHIFT:
            if e.key in [K_RIGHT, K_LEFT]:
                if AXIS1 is not None and AXIS2 is not None:
                    AXIS1, AXIS2 = AXIS2, AXIS1

            if e.key == K_UP:
                AXIS1, AXIS2, INDEX = INDEX, AXIS1, AXIS2
            if e.key == K_DOWN:
                INDEX, AXIS1, AXIS2 = AXIS1, AXIS2, INDEX

            if e.key in [K_RIGHT, K_LEFT, K_UP, K_DOWN]:
                view_changed = True
                
        elif e.type == KEYDOWN:
            if e.key == K_COMMA: gif=True

            if e.key == K_EQUALS: PW += 1
            if e.key == K_MINUS: PW = max(1, PW - 1)
            if e.key in [K_EQUALS, K_MINUS]:
                view_changed = True

            if e.key == K_f:
                inputs.input_frame(SCREEN, FONTS[FONT], SCREEN, draw)

            if e.key == K_c:
                inputs.input_cube(SCREEN, FONTS[FONT], SCREEN, draw)

            if e.key == K_p:
                inputs.input_plane(SCREEN, FONTS[FONT], SCREEN, draw)

            if e.key == K_b:
                inputs.input_build(SCREEN, FONTS[FONT], SCREEN, draw)

        elif e.type == MOUSEMOTION:
            MPOS = e.pos

        if board_changed:
            frames.update_all()
        if view_changed and name is not None:
            frames.update_frame(name, pixelwidth=PW, axis1=AXIS1, axis2=AXIS2, index=INDEX)

def draw(dest):
    dest.fill((100, 100, 100))
    name = frames.get_frame_at(MPOS) if MPOS is not None else None
    for frame in frames.get_frame_names():
        col = (0, 0, 0) if frame != name else (0, 200, 0)
        frames.draw_frame(dest, frame, FONTS[FONT], col)

while __name__ == "__main__":
    draw(SCREEN)
    pygame.display.update()
    process()

