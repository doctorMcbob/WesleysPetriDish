import pygame
from pygame import Rect
from pygame.locals import *

from display import get_view, drawn_view
import printer
import cubes

frames = {}

order = ["x", "y", "z", "a", "b", "c", "d", "e", "f", "g"]
styles = ["animation", "list"]

def add_frame(name, position, dimensions, pixelwidth,
              cube, style, axis1, axis2, index, padding=4):
    frames[name] = {
        "cube": cube,
        "views": [],
        "position": position,
        "dimensions": dimensions,
        "viewpos": tuple(0 for _ in range(len(cubes.get_cube_dimensions(cube)))),
        "axis1": axis1,
        "axis2": axis2,
        "index": index,
        "padding": padding,
        "style": style,
        "pixelwidth": pixelwidth,
    }
    if style == "animation":
        frames[name]["frame"] = 0
    update_frame(name)
        
def draw_frame(dest, name, font, box=False):
    frame = frames[name]
    ax1, ax2, ax3 = frame["axis1"], frame["axis2"], frame["index"]
    width, height = frame["dimensions"]
    x, y = frame["position"]
    if box:
        pygame.draw.rect(dest, box, Rect((x, y), (width, height)), width=2)
        x+=8
        y+=8
    dest.blit(font.render(name, 0, (0, 0, 0)), (x, y))
    dest.blit(font.render(frame["style"], 0, (0, 0, 0)), (x, y + 16))
    dest.blit(font.render("{}".format(frame["viewpos"]), 0, (0, 0, 0)), (x+64, y))
    dest.blit(font.render("axis1: {}".format(order[frame["axis1"]]), 0, (0, 0, 0)), (x+128, y + 16))
    dest.blit(font.render("axis2: {}".format(order[frame["axis2"]]), 0, (0, 0, 0)), (x+256, y + 16))
    dest.blit(font.render("index: {}".format(order[frame["index"]]), 0, (0, 0, 0)), (x+384, y + 16))
    y += 64
        
    if frame["style"] == "list":
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

    elif frame["style"] == "animation":
        view = frame["views"][frame["frame"] % len(frame["views"])]
        frame["frame"] += 1
        drawn = drawn_view(view, pixelwidth=frame["pixelwidth"], off=(110, 110, 180), on=(255, 200, 200))
        dest.blit(drawn, (x, y))

def update_all():
    for name in frames:
        update_frame(name)

def get_frame_names():
    return list(frames.keys())

def update_frame(name,
                 cube=None, pixelwidth=None,
                 viewpos=None, position=None, dimensions=None,
                 axis1=None, axis2=None, index=None):
    frame = frames[name]
    frame["cube"] = cube if cube is not None else frame["cube"]
    frame["dimensions"] = dimensions if dimensions is not None else frame["dimensions"]
    frame["viewpos"] = viewpos if viewpos is not None else frame["viewpos"]
    frame["axis1"] = axis1 if axis1 is not None else frame["axis1"]
    frame["axis2"] = axis2 if axis2 is not None else frame["axis2"]
    frame["index"] = index if index is not None else frame["index"]
    ax1, ax2, ax3 = frame["axis1"], frame["axis2"], frame["index"]
    frame["pixelwidth"] = pixelwidth if pixelwidth is not None else frame["pixelwidth"]

    i = len(frame["viewpos"]) - 1
    cube = cubes.get_cube(frame["cube"])
    dimensions = []
    head = cube
    while i >= 0:
        dimensions.append(len(head))
        head = head[0]
        i -= 1
    dimensions = dimensions[::-1]
    width = dimensions[ax3]
    frame["views"] = []
    for i in range(width):
        viewpos = tuple([v + (i * (_i == ax3)) for _i, v in enumerate(frame["viewpos"])])
        frame["views"].append(get_view(cube, viewpos, ax1, ax2))

def get_frame_at(pos):
    for name in frames:
        frame = frames[name]
        rect = Rect(frame["position"], frame["dimensions"])

        if rect.collidepoint(pos):
            return name
    return None

def get_frame_data(name):
    return frames[name]

def export_to_gif(name):
    frame = frames[name]
    for view in frame["views"]:
        printer.save_surface(
            drawn_view(view, pixelwidth=frame["pixelwidth"], off=(110, 110, 180), on=(255, 200, 200)))
    printer.save_em()
    printer.make_gif()
    printer.clear_em()
    

