import pygame
from pygame import Rect, Surface
from pygame.locals import *

import sys

from multiarray import ndimensional
from utils import getAt, setAt, points_in_dimensions, nbrsnd
from display import drawn_view, get_view
import frames
import cubes
import automata

NUMBERS_ONLY = {
    K_0: "0", K_1: "1", K_2: "2", K_3: "3", K_4: "4",
    K_5: "5", K_6: "6", K_7: "7", K_8: "8", K_9: "9",
}

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
                
def get_text_input(dest, font, pos, numeric=False):
    string = ''
    KEY_MAP = NUMBERS_ONLY if numeric else ALPHABET_KEY_MAP
    while True:
        surf = Surface((256, 32))
        surf.fill((230, 230, 230))
        surf.blit(font.render(string, 0, (0, 0, 0)), (0, 0))
        dest.blit(surf, pos)
        pygame.display.update()

        inp = expect_input()
        if inp == K_ESCAPE: return None
        if inp == K_BACKSPACE: string = string[:-1]
        if inp == K_RETURN: return int(string) if numeric else string 

        if pygame.key.get_mods() & KMOD_SHIFT and not numeric:
            if inp in ALPHABET_SHIFT_MAP:
                string = string + ALPHABET_SHIFT_MAP[inp]
            elif inp in KEY_MAP:
                string = string + KEY_MAP[inp].upper()
        elif inp in KEY_MAP:
            string = string + KEY_MAP[inp]

def select_from_list(dest, position, font, l, args=None, cb=lambda *args: None):
    idx = 0
    if not l: return None
    while True:
        surf = Surface((256, 32*len(l)))
        surf.fill((230, 230, 230))
        cb(args)
        for i, text in enumerate(l):
            col = (0, 0, 0) if i != idx else (160, 110, 190)
            surf.blit(font.render(str(text), 0, col), (0, i*32))
        dest.blit(surf, position)
        inp = expect_input()

        if inp == K_UP: idx -= 1
        if inp == K_DOWN: idx += 1
        if inp in [K_RETURN, K_SPACE]: return l[idx]
        if inp in [K_ESCAPE, K_BACKSPACE] or not l: return None
        idx %= len(l)
    
def input_rect(dest, font=None, snap=16, args=None, cb=lambda *args:None):
    if font is not None: dest.blit(font.render("CLICK TWICE FOR RECT", 0, (0, 0, 0)), (0, 0))
    def draw_helper(args):
        cb(args)
        mpos = pygame.mouse.get_pos()
        dest.blit(
            font.render(
                "{},{}".format((mpos[0] // snap)*snap, (mpos[1] // snap)*snap),
                0, (0, 0, 0)),
            (0, 0))
    pos, btn = expect_click(args, draw_helper)
    if not pos: return None, None
    pos = (pos[0] // snap)*snap, (pos[1] // snap)*snap
    def draw_helper2(args):
        draw_helper(args)
        pos2 = pygame.mouse.get_pos()
        x1 = min(pos[0], pos2[0])
        x2 = max(pos[0], pos2[0])
        y1 = min(pos[1], pos2[1])
        y2 = max(pos[1], pos2[1])
        pygame.draw.rect(dest, (0, 150, 0), Rect((x1, y1), ((x2-x1), (y2-y1))), width=2)
    pos2, btn2 =  expect_click(args, draw_helper2)
    if not pos2: return None, None
    pos2 = (pos2[0] // snap)*snap, (pos2[1] // snap)*snap
    x1 = min(pos[0], pos2[0])
    x2 = max(pos[0], pos2[0])
    y1 = min(pos[1], pos2[1])
    y2 = max(pos[1], pos2[1])
    return (x1, y1), ((x2 - x1), (y2 - y1))
    
def input_frame(dest, font, args=None, cb=lambda *args: None):
    cb(args)
    dest.blit(font.render("Name:", 0, (0, 0, 0)), (0, 0))
    name = get_text_input(dest, font, (64, 0))
    cb(args)
    if name is None: return None
    pos, dim = input_rect(dest, font, args=args, cb=cb)
    cb(args)
    if pos is None: return None
    dest.blit(font.render("Style:", 0, (0, 0, 0)), (0, 0))
    cb(args)
    style = select_from_list(dest, (64, 32), font, frames.styles)
    if style is None: return None
    cb(args)
    dest.blit(font.render("Cube:", 0, (0, 0, 0)), (0, 0))
    cube = select_from_list(dest, (64, 32), font, cubes.get_cube_names())
    cb(args)
    if cube is None: return None
    dimensions = cubes.get_cube_dimensions(cube)
    cb(args)
    dest.blit(font.render("Axis 1:", 0, (0, 0, 0)), (0, 0))
    letter = select_from_list(dest, (64, 32), font, frames.order[:len(dimensions)])
    cb(args)
    if letter is None: return None
    ax1 = frames.order.index(letter)
    cb(args)
    dest.blit(font.render("Axis 2:", 0, (0, 0, 0)), (0, 0))
    letter = select_from_list(dest, (64, 32), font, frames.order[:len(dimensions)])
    cb(args)
    if letter is None: return None
    ax2 = frames.order.index(letter)
    cb(args)
    dest.blit(font.render("Index:", 0, (0, 0, 0)), (0, 0))
    letter = select_from_list(dest, (64, 32), font, frames.order[:len(dimensions)])
    cb(args)
    if letter is None: return None
    idx = frames.order.index(letter)
    return frames.add_frame(dest, font, name, pos, dim, 4, cube, style, ax1, ax2, idx)
    

def input_board(dest, position, dim, startfrom=False, style='bool', pixelwidth=16, args=None, cb=lambda *args: None):
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
                if e.key == K_ESCAPE: return None
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
                pos = (px-x) // pixelwidth, (py-y) // pixelwidth
                if style=='bool': setAt(board, pos, int(not getAt(board, pos)))
                if style.startswith('int'): setAt(board, pos, (getAt(board, pos) + 1) % int(style.split(":")[-1]))


def input_cube(dest, font, args=None, cb=lambda *args: None):
    cb(args)
    dest.blit(font.render("Name:", 0, (0, 0, 0)), (0, 0))
    name = get_text_input(dest, font, (64, 0))
    if name is None: return None
    cb(args)
    dest.blit(font.render("Dimensions:", 0, (0, 0, 0)), (0, 0))
    n = get_text_input(dest, font, (64, 0), True)
    if n is None or n >= len(frames.order): return None
    dimensions = []
    for i in range(n):
        cb(args)
        dest.blit(font.render(frames.order[i], 0, (0, 0, 0)), (0, 0))
        d = get_text_input(dest, font, (64, 0), True)
        if d is None: return None
        dimensions.append(d)
    dimensions = tuple(dimensions)
    cubes.add_cube(name, n, dimensions)

def input_plane(dest, font, args=None, cb=lambda *args: None):
    cb(args)
    dest.blit(font.render("Name:", 0, (0, 0, 0)), (0, 0))
    name = get_text_input(dest, font, (64, 0))
    if name is None: return None
    cb(args)
    dest.blit(font.render("Width:", 0, (0, 0, 0)), (0, 0))
    W = get_text_input(dest, font, (64, 0), True)
    if W is None: return None
    cb(args)
    dest.blit(font.render("Height:", 0, (0, 0, 0)), (0, 0))
    H = get_text_input(dest, font, (64, 0), True)
    if H is None: return None
    cb(args)
    cube = input_board(dest, (64, 64), (W, H), args=args, cb=cb)
    if cube is None: return None
    return cubes.add_pre_built(name, (W, H), cube)

def input_build(dest, font, args=None, cb=lambda *args: None):
    cb(args)
    dest.blit(font.render("Name:", 0, (0, 0, 0)), (0, 0))
    name = get_text_input(dest, font, (64, 0))
    if name is None: return None
    cb(args)
    dest.blit(font.render("Seed:", 0, (0, 0, 0)), (0, 0))
    seed = select_from_list(dest, (64, 32), font, cubes.get_cube_names())
    if seed is None: return None
    cb(args)
    dest.blit(font.render("Length:", 0, (0, 0, 0)), (0, 0))
    length = get_text_input(dest, font, (64, 0), True)
    if length is None: return None
    cb(args)
    dest.blit(font.render("Rule:", 0, (0, 0, 0)), (0, 0))
    rule = select_from_list(dest, (64, 32), font, automata.get_rule_names())
    if rule is None: return None
    return cubes.build_cube(name, seed, length, rule)

def input_save_frame(dest, font, args=None, cb=lambda *args: None):
    cb(args)
    dest.blit(font.render("Name:", 0, (0, 0, 0)), (0, 0))
    name = get_text_input(dest, font, (64, 0))
    if name is None: return None
    return frames.save_frames_as(name)

def input_load_frame(dest, font, args=None, cb=lambda *args: None):
    cb(args)
    dest.blit(font.render("Name:", 0, (0, 0, 0)), (0, 0))
    name = select_from_list(dest, (64, 32), font, frames.get_context_names())
    if name is None: return None
    return frames.load_frames(name)
    
def input_generic_rule(dest, font, args=None, cb=lambda *args: None):
    cb(args)
    dest.blit(font.render("Name:", 0, (0, 0, 0)), (0, 0))
    name = get_text_input(dest, font, (64, 0))
    if name is None: return None
    cb(args)
    dest.blit(font.render("N dimension:", 0, (0, 0, 0)), (0, 0))
    n = get_text_input(dest, font, (64, 0), True)
    if n is None or n >= len(frames.order): return None
    cb(args)
    dest.blit(font.render("Inverted? Y/N", 0, (0, 0, 0)), (0, 0))
    inverted = expect_input() == K_y
    ruleset = set()

    rulesegment = input_rule_segment(dest, font, args=args, cb=cb, n=n)
    while rulesegment is not None:
        ruleset.add(rulesegment)
        rulesegment = input_rule_segment(dest, font, args=args, cb=cb, n=n)
    
    automata.RULE_SETS[name] = ruleset
    automata.RULES[name] = automata.make_generic_ndimensional(name, n, ruleset, inverted)
    return "Rule {} created with ruleset size {} inverted? {}".format(name, len(ruleset), inverted)

def input_rule_segment(dest, font, args=None, cb=lambda *args: None, n=2):
    if n==1: return input_1d_rule(dest, font, args, cb)
    board = ndimensional(n, tuple(3 for _ in range(n)), filler=0)
    setAt(board, [1 for _ in range(n)], 2)
    done = False
    while not done:
        cb(args)
        points = points_in_dimensions(3 for n in range(2, n))
        corners = []
        if not points: points.append([])
        x, y = 16, 16
        for point in points:
            pos = [0, 0] + point
            view = get_view(board, pos, tuple(3 for _ in range(n)), 0, 1)
            drawn = drawn_view(view, pixelwidth=16)
            text = font.render("{}".format(pos[2:]), 0, (0, 0, 0))
            if x + max((drawn.get_width(), text.get_width())) > dest.get_width():
                x = 16
                y += drawn.get_height() + 32
            if y + drawn.get_height() + 32 > dest.get_height():
                break
            dest.blit(text, (x, y))
            dest.blit(drawn, (x, y+32))
            corners.append((x, y+32))
            x += max((drawn.get_width(), text.get_height())) + 32
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == QUIT: sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE: return None
                if e.key == K_RETURN: done = True
            if e.type == MOUSEBUTTONDOWN:
                x, y = e.pos

                for i, point in enumerate(points):
                    left, top = corners[i]

                    if left > x or x > left+16*3 or top > y or y > top+16*3:
                        continue
                    
                    pos = [
                        (y - top) // 16,
                        (x - left) // 16,
                    ] + point

                    value = getAt(board, pos)
                    if value is None: continue
                    setAt(board, pos, (value + 1)%3)

    serialized = ""
    center = tuple(1 for _ in range(n))
    for pos in nbrsnd(center):
        at = getAt(board, pos)
        if at == 2: at = "?"
        serialized += "{}".format(at)
    return serialized

def input_1d_rule(dest, font, args=None, cb=lambda *args: None):
    a, b, c = 0, 0, 0
    done = False
    cols = [(255, 255, 255), (0, 0, 0), (125, 125, 125)]
    while not done:
        cb(args)
        pygame.draw.rect(dest, cols[a], Rect((16, 16), (32, 32)))
        pygame.draw.rect(dest, cols[b], Rect((48, 16), (32, 32)))
        pygame.draw.rect(dest, cols[c], Rect((80, 16), (32, 32)))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == QUIT: sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE: return None
                if e.key == K_RETURN: done = True

            if e.type == MOUSEBUTTONDOWN:
                x, y = e.pos
                if 16 > x or x > 112 or 16 > y or y > 48:
                    continue
                if 48 > x: a = (a + 1) % 3
                elif 80 > x: b = (b + 1) % 3
                else: c = (c + 1) % 3
    a = "?" if a == 2 else a
    b = "?" if b == 2 else b
    c = "?" if c == 2 else c

    return "{}{}{}".format(a, b, c)

def input_slice(dest, font, args=None, cb=lambda *args: None):
    cb(args)
    dest.blit(font.render("Name:", 0, (0, 0, 0)), (0, 0))
    name = get_text_input(dest, font, (64, 0))
    if name is None: return None
    cb(args)
    dest.blit(font.render("Cube:", 0, (0, 0, 0)), (0, 0))
    cube = select_from_list(dest, (64, 32), font, cubes.get_cube_names())
    if cube is None: return None
    cb(args)
    dest.blit(font.render("Index:", 0, (0, 0, 0)), (0, 0))
    idx =  select_from_list(dest, (64, 32), font, list(range(len(cubes.get_cube(cube)))))
    if idx is None: return None

    return cubes.make_slice(name, cube, idx)

def input_splay(dest, font, args=None, cb=lambda *args: None):
    cb(args)
    dest.blit(font.render("Name:", 0, (0, 0, 0)), (0, 0))
    name = get_text_input(dest, font, (64, 0))
    cb(args)
    if name is None: return None
    pos, dim = input_rect(dest, font, args=args, cb=cb)
    cb(args)
    if pos is None: return None
    dest.blit(font.render("Style:", 0, (0, 0, 0)), (0, 0))
    cb(args)
    style = select_from_list(dest, (64, 32), font, frames.styles)
    if style is None: return None
    cb(args)
    dest.blit(font.render("Cube:", 0, (0, 0, 0)), (0, 0))
    cube = select_from_list(dest, (64, 32), font, cubes.get_cube_names())
    cb(args)
    if cube is None: return None
    dimensions = cubes.get_cube_dimensions(cube)
    cb(args)
    dest.blit(font.render("Axis 1:", 0, (0, 0, 0)), (0, 0))
    letter = select_from_list(dest, (64, 32), font, frames.order[:len(dimensions)])
    cb(args)
    if letter is None: return None
    ax1 = frames.order.index(letter)
    cb(args)
    dest.blit(font.render("Axis 2:", 0, (0, 0, 0)), (0, 0))
    letter = select_from_list(dest, (64, 32), font, frames.order[:len(dimensions)])
    cb(args)
    if letter is None: return None
    ax2 = frames.order.index(letter)
    cb(args)
    dest.blit(font.render("Index:", 0, (0, 0, 0)), (0, 0))
    letter = select_from_list(dest, (64, 32), font, frames.order[:len(dimensions)])
    cb(args)
    if letter is None: return None
    idx = frames.order.index(letter)
    dest.blit(font.render("Splay:", 0, (0, 0, 0)), (0, 0))
    letter = select_from_list(dest, (64, 32), font, frames.order[:len(dimensions)])
    sdx = frames.order.index(letter)
    cb(args)
    if letter is None: return None
    splay = frames.order.index(letter)

    head = cubes.get_cube(cube)
    i = 0

    while i < len(dimensions) - sdx-1:
        head = head[0]
        i += 1

    x, y = pos
    w, h = dim
    for i, cube_segment in enumerate(head):
        segment_name = "{name}{i}".format(name=name, i=i)
        cubes.add_pre_built(segment_name, dimensions[:sdx], cube_segment)
        frames.add_frame(dest, font, segment_name, (x, y), (w, h), 4, segment_name, style, ax1, ax2, idx)
        x += w

    return "Splayed {} across {} frames".format(cube, len(head))
    
def input_delete_frame(dest, font, args=None, cb=lambda *args: None):
    cb(args)
    dest.blit(font.render("Frame:", 0, (0, 0, 0)), (0, 0))
    frame = select_from_list(dest, (64, 32), font, frames.get_frame_names())
    if frame is None: return None
    return frames.delete_frame(frame)
