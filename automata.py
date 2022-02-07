from multiarray import ndimensional

from utils import nbrs2d, getAt, setAt

def life2d(board):
    new = ndimensional(2, len(board), filler=0)
    for x in range(len(board)):
        for y in range(len(board)):
            n = sum([1 if getAt(board, pos) else 0 for pos in nbrs2d(x, y)])
            if (n == 2 and getAt(board, (x, y))) or (n==3):
                setAt(new, (x, y), 1)
    return new

