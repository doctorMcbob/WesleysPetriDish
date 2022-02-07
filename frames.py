import pygame
from pygame.locals import *

from display import get_view, drawn_view

frames = {}

order = ["x", "y", "z", "a", "b", "c", "d", "e", "f", "g"]

def add_frame(name, position, pixelwidth, cube, style, viewpos, axis1, axis2, axis3, padding=4):
    """
    name - string identifier
    position - where on screen
    pixelwidth - width of each pixel
    cube - for refrence
    style - options:
       "animation",
       "list:w,h"
    """
    frames[name] = {
        "cube": cube,
        "views": [],
        "position": position,
        "viewpos": viewpos,
        "axis1": axis1,
        "axis2": axis2,
        "axis3": axis3,
        "padding": padding,
        "style": style,
        "pixelwidth": pixelwidth,
    }
    if style.startswith("list"):
        noun, data = style.split(":")
        frames[name]["style"] = noun
        w, h = data.split(",")
        frames[name]["dimensions"] = int(w), int(h)
    if style == "animation":
        frames[name]["frame"] = 0
    update_frame(name)
        
def draw_frame(dest, name, font, box=False):
    frame = frames[name]
    ax1, ax2, ax3 = frame["axis1"], frame["axis2"], frame["axis3"]
    if frame["style"] == "list":
        width, height = frame["dimensions"]
        x, y = frame["position"]
        if box:
            pygame.draw.rect(dest, box, Rect((x, y), (width, height)), width=2)
            x+=8
            y+=8
        y += 32
        for i, view in enumerate(frame["views"]):
            drawn = drawn_view(view, pixelwidth=frame["pixelwidth"], off=(110, 110, 180), on=(255, 200, 200))
            if x + drawn.get_width() + frame["padding"] > frame["position"][0] + width:
                x = frame["position"][0]
                if box: x += 8
                y += drawn.get_height() + frame["padding"]
            if y + drawn.get_height() + frame["padding"] > frame["position"][1] + height:
                break
            dest.blit(drawn, (x, y))
            x += drawn.get_width() + frame["padding"]
    dest.blit(font.render(name, 0, (0, 0, 0)), frame["position"])
    dest.blit(font.render(frame["style"], 0, (0, 0, 0)), (frame["position"][0], frame["position"][1] + 16))
    
def update_frame(name,
                 cube=None, pixelwidth=None,
                 viewpos=None, position=None, dimensions=None,
                 axis1=None, axis2=None, axis3=None):
    frame = frames[name]
    frame["cube"] = cube if cube is not None else frame["cube"]
    frame["dimensions"] = dimensions if dimensions is not None else frame["dimensions"]
    frame["viewpos"] = viewpos if viewpos is not None else frame["viewpos"]
    frame["axis1"] = axis1 if axis1 is not None else frame["axis1"]
    frame["axis2"] = axis2 if axis2 is not None else frame["axis2"]
    frame["axis3"] = axis3 if axis3 is not None else frame["axis3"]
    ax1, ax2, ax3 = frame["axis1"], frame["axis2"], frame["axis3"]
    frame["pixelwidth"] = pixelwidth if pixelwidth is not None else frame["pixelwidth"]
    i = len(frame["viewpos"]) - 1
    dimensions = []
    head = frame["cube"]
    while i >= 0:
        dimensions.append(len(head))
        head = head[0]
        i -= 1
    dimensions = dimensions[::-1]
    width = dimensions[ax3]
    frame["views"] = []
    for i in range(width):
        viewpos = tuple([v + (i * (_i == ax3)) for _i, v in enumerate(frame["viewpos"])])
        frame["views"].append(get_view(frame["cube"], viewpos, ax1, ax2))

