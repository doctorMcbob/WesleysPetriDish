import pygame
from pygame.locals import *
from pygame import Surface, Rect

import os
import sys
from datetime import datetime

from pysrc.multiarray import ndimensional
from pysrc.utils import getAt, setAt

def get_view(multiarray, position, dimensions, axis1, axis2):
    view = []
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

def drawn_view(view,
               pixelwidth=32, off=(255, 255, 255),
               on=(0, 0, 0), bg=(120, 120, 120), other=(120, 120, 120)):
    surf = Surface((len(view[0])*pixelwidth, len(view)*pixelwidth))
    for x, row in enumerate(view):
        for y, slot in enumerate(row):
            col = on if slot == 1 else other
            if not slot: col = off
            if view[x][y] is None: col = bg
            pygame.draw.rect(surf, col, Rect((y*pixelwidth, x*pixelwidth), (pixelwidth, pixelwidth)))
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

