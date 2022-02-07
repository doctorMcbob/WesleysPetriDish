import pygame
from pygame.locals import *
from pygame import Surface, Rect

import os
import sys
from datetime import datetime

from multiarray import ndimensional
from utils import getAt, setAt

def get_view(multiarray, position, axis1, axis2):
    view = []
    i = len(position)-1
    head = multiarray
    dimensions = []
    while i >= 0:
        dimensions.append(len(head))
        head = head[0]
        i -= 1
    dimensions = dimensions[::-1]
    width = dimensions[axis1]
    height = dimensions[axis2]
    x = position[axis1]
    y = position[axis2]
    for dx in range(width):
        view.append([])
        for dy in range(height):
            pos = list(position)
            pos[axis1] = x+dx
            pos[axis2] = y+dy
            pos = tuple(pos)
            view[-1].append(getAt(multiarray, pos))
    return view

def drawn_view(view, pixelwidth=32, off=(255, 255, 255), on=(0, 0, 0), bg=(120, 120, 120)):
    surf = Surface((len(view)*pixelwidth, len(view[0])*pixelwidth))
    for x in range(len(view)):
        for y in range(len(view[0])):
            col = on if view[x][y] else off
            if view[x][y] is None: col = bg
            pygame.draw.rect(surf, col, Rect((x*pixelwidth, y*pixelwidth), (pixelwidth, pixelwidth)))
    return surf

def pretty_print_view(view):
    s = ""
    sprites = " X0Oo."
    for row in view:
        for slot in row:
            s += sprites[slot]+"," if slot else " ,"
        s+= "\n"
    print(s)

def screenshot(surf, name=None):
    if not os.path.isdir("pics/"): os.mkdir("pics/")
    s = "pics/"+name+".png" if name is not None else "pics/snapshot{}.png".format(datetime.now())
    print(s)
    pygame.image.save(surf, s)

def input_board(dest, position, width, height, startfrom=False, style='bool', pixelwidth=16, args=None, cb=lambda *args: None):
    """style bool is a toggle 0/1, style int requires syntax int:9 for upper bound of 9"""
    board = startfrom or ndimensional(2, diameter, filler=0)
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
