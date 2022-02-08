import pygame
from pygame import Rect
from pygame.locals import *

import sys

from multiarray import ndimensional
from utils import getAt, setAt
from display import drawn_view
import frames

ALPHABET_KEY_MAP = {
    K_a: "a", K_b: "b", K_c: "c", K_d: "d", K_e: "e",
    K_f: "f", K_g: "g", K_h: "h", K_i: "i", K_j: "j",
    K_k: "k", K_l: "l", K_m: "m", K_n: "n", K_o: "o",
    K_p: "p", K_q: "q", K_r: "r", K_s: "s", K_t: "t",
    K_u: "u", K_v: "v", K_w: "w", K_x: "x", K_y: "y",
    K_z: "z", K_SPACE: " ",
    K_0: "0", K_1: "1", K_2: "2", K_3: "3", K_4: "4",
    K_5: "5", K_6: "6", K_7: "7", K_8: "8", K_9: "9",
    K_EQUALS: "=", K_MINUS: "-", K_COLON: ";", K_PERIOD:".",
    K_LEFTPAREN: "(", K_RIGHTPAREN: ")", K_COMMA: ",",
    K_ASTERISK: "*", K_SLASH: "/"
}

ALPHABET_SHIFT_MAP = {
    K_0: ")", K_1: "!", K_2: "@", K_3: "#", K_4: "$",
    K_5: "%", K_6: "^", K_7: "&", K_8: "*", K_9: "(",
    K_EQUALS: "+", K_MINUS: "_", K_COLON: ":", K_PERIOD:">",
    K_COMMA: "<", K_SLASH: "?"
}

def expect_click(args=None, cb=lambda *args: None):
    while True:
        cb(args)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == QUIT: return None, None
            if e.type == KEYDOWN and e.key == K_ESCAPE: return None, None
            if e.type == MOUSEBUTTONDOWN:
                return e.pos, e.button

def expect_input(expectlist=[], args=None, cb=lambda *args:None):
    cb(args)
    while True:
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == QUIT:
                return None
            if e.type == KEYDOWN:
                if expectlist:
                    if e.key in expectlist: return e.key
                else: return e.key

def select_from_list(dest, position, font, l, args=None, cb=None):
    idx = 0
    if not l: return None
    while True:
        surf = Surface((256, 32*len(l)))
        surf.fill((230, 230, 230))
        cb(args)
        for i, text in enumerate(l):
            col = (0, 0, 0) if i != idx else (160, 110, 190)
            surf.blit(font.render(str(text), 0, col), (0, i*32))
        dest.blit(surf, pos)
        inp = expect_input()

        if inp == K_UP: idx -= 1
        if inp == K_DOWN: idx += 1
        if inp in [K_RETURN, K_SPACE]: return list[idx]
        if inp in [K_ESCAPE, K_BACKSPACE] or not list: return None
        idx %= len(list)
    
def input_rect(dest, font=None, snap=16, args=None, cb=lambda *args:None):
    if font is not None: dest.blit(font.render("CLICK TWICE FOR RECT", 0, (0, 0, 0)), (0, 0))
    def draw_helper(args):
        cb(args)
        mpos = pygame.mouse.get_pos()
        dest.blit(font.render("{}".format(((mpos[0] // snap)*snap, (mpos[1] // snap)*snap)), 0, (0, 0, 0)), (0, 0))
    pos, btn = expect_click(args, draw_helper)
    if not pos: return None, None
    def draw_helper2(args):
        draw_helper(args)
        pos2 = pygame.mouse.get()
        x1 = min(pos[0], pos2[0])
        x2 = max(pos[0], pos2[0])
        y1 = min(pos[1], pos2[1])
        y2 = max(pos[1], pos2[1])
        pygame.draw.rect(dest, (0, 150, 0), Rect((x1, y1), ((x2-x1), (y2-y1))))
    pos2, btn2 =  expect_click(args, draw_helper2)
    if not pos2: return None, None
    x1 = min(pos[0], pos2[0])
    x2 = max(pos[0], pos2[0])
    y1 = min(pos[1], pos2[1])
    y2 = max(pos[1], pos2[1])
    return (x1, y1), ((x2 - x1), (y2 - y1))
    
def input_frame(dest, font, args=None, cb=lambda *args: None):
    pos, dim = input_rect(dest, font, args, cb)
    if pos is None: return None
    dest.blit(font.render("Style:", 0, (0, 0, 0)), (0, 0))
    style = select_from_list(dest, (64, 32), font, frames.styles)
    if style is None: return None
    dest.blit(font.render("Cube:", 0, (0, 0, 0)), (0, 0))
    cube = select_from_list(des, (64, 32), font, cubes.get_cube_names())
    if cube is None: return None

def input_board(dest, position, dim, startfrom=False, style='bool', pixelwidth=16, args=None, cb=lambda *args: None):
    """style bool is a toggle 0/1, style int requires syntax int:9 for upper bound of 9"""
    width, height = dim
    board = startfrom or ndimensional(2, dim, filler=0)
    while True:
        cb(args)
        dest.blit(drawn_view(board, pixelwidth=pixelwidth), position)
        pygame.display.update()
        pos = 0, 0
        for e in pygame.event.get():
            if e.type == QUIT: sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE: sys.exit()
                if e.key == K_LEFT: pos = pos[0] - 1, pos[1]
                if e.key == K_UP: pos = pos[0], pos[1] - 1
                if e.key == K_RIGHT: pos = pos[0] + 1, pos[1]
                if e.key == K_DOWN: pos = pos[0], pos[1] + 1
                if e.key == K_SPACE:
                    if style=='bool': setAt(board, pos, int(not getAt(board, pos)))
                    if style.startswith('int'): setAt(board, pos, (getAt(board, pos) + 1) % int(style.split(":")[-1]))
                if e.key == K_RETURN:
                    return board
            if e.type == MOUSEMOTION:
                x, y = position
                px, py = e.pos
                if x > px or y > py or px > x+width*pixelwidth or py > y+height*pixelwidth:
                    continue
                pos = (px-x) // pixelwidth, (py-y) // pixelwidth
            if e.type == MOUSEBUTTONDOWN:
                x, y = position
                px, py = e.pos
                if not (x < px < x+width*pixelwidth and y < py < y+height*pixelwidth):
                    continue
                pos = (py-y) // pixelwidth, (px-x) // pixelwidth
                if style=='bool': setAt(board, pos, int(not getAt(board, pos)))
                if style.startswith('int'): setAt(board, pos, (getAt(board, pos) + 1) % int(style.split(":")[-1]))
