from multiarray import ndimensional

from utils import nbrs2d, getAt, setAt

def get_rule_names():
    return list(RULES.keys())

def life2d(board, dimensions):
    new = ndimensional(2, dimensions, filler=0)
    for x in range(dimensions[0]):
        for y in range(dimensions[1]):
            n = sum([1 if getAt(board, pos) else 0 for pos in nbrs2d(x, y)])
            if (n == 2 and getAt(board, (x, y))) or (n==3):
                setAt(new, (x, y), 1)
    return new

RULES = {
    "life": life2d,
}

