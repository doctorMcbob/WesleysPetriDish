"""
export frames as images
"""
import os
import sys
import imageio
import pygame
from pygame.locals import *
from pathlib import Path
from datetime import datetime

ROOT_PATH = Path('.')
PATH_TO_REPLAY = ROOT_PATH / ("gifs/" if "-o" not in sys.argv else "gifs/" + sys.argv[sys.argv.index("-o") + 1])
PATH_TO_DUMP = ROOT_PATH / ("gifs/dump")

if not os.path.isdir(PATH_TO_REPLAY): os.mkdir(PATH_TO_REPLAY)
if not os.path.isdir(PATH_TO_DUMP): os.mkdir(PATH_TO_DUMP)

FRAME = 0
SAVED = []

START = None

def save_surface(surf):
    w, h = (surf.get_width(), surf.get_height())
    save = pygame.Surface((w, h))
    save.blit(surf, (0, 0))
    SAVED.append(save)

def save_em():
    global SAVED
    for i, surf in enumerate(SAVED):
        pygame.image.save(surf, str(PATH_TO_DUMP/"{}.png".format(i)))
    SAVED = []
        
def make_gif(filename=None, fps=15):
    if filename is None:
        filename = "{}.gif".format(datetime.now())
    images = []
    num_imgs = len(os.listdir(ROOT_PATH / PATH_TO_DUMP))
    for i in range(num_imgs):
        file_name = "{}.png".format(i)
        file_path = os.path.join(ROOT_PATH / PATH_TO_DUMP, file_name)
        images.append(imageio.imread(file_path))
    imageio.mimsave(os.path.join(ROOT_PATH / PATH_TO_REPLAY, filename), images, fps=fps)
    return str(os.path.join(ROOT_PATH / PATH_TO_REPLAY, filename))

def clear_em():
    num_imgs = len(os.listdir(ROOT_PATH / PATH_TO_DUMP))
    for i in range(num_imgs):
        file_name = "{}.png".format(i)
        file_path = os.path.join(ROOT_PATH / PATH_TO_DUMP, file_name)
        os.remove(file_path)
