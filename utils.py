from random import randint
from copy import deepcopy

def getAt(multiarray, position):
    axis = len(position)-1
    head = multiarray
    try:
        while axis > 0:
            if position[axis] < 0: return None
            head = head[position[axis]]
            axis -= 1
        if position[axis] < 0: return None
        return head[position[axis]]
    except IndexError:
        return None

def setAt(multiarray, position, value):
    axis = len(position)-1
    head = multiarray
    while axis > 0:
        head = head[position[axis]]
        axis -= 1
    head[position[axis]] = value
    
def nbrs2d(x, y):
    yield x-1, y-1
    yield x-1, y
    yield x-1, y+1
    yield x, y-1
    yield x, y+1
    yield x+1, y-1
    yield x+1, y
    yield x+1, y+1

def nbrsnd(pos):
    positions = [[]]
    for v in pos:
        for idx in range(len(positions)):
            slot1 = positions[idx]
            slot2 = deepcopy(positions[idx])
            slot3 = deepcopy(positions[idx])
            slot1.append(v-1)
            slot2.append(v)
            slot3.append(v+1)
            positions.append(slot2)
            positions.append(slot3)
    return positions

def points_in_dimensions(dimensions):
    positions = [[]]
    dimensions = list(dimensions)
    while dimensions:
        d_ = dimensions.pop(0) - 1
        for idx in range(len(positions)):
            positions[idx]
            d = d_
            d -= 1
            while d >= 0:
                slot = deepcopy(positions[idx])
                slot.append(d)
                positions.append(slot)
                d -= 1
            positions[idx].append(d_)
    return positions

def randomize2d(board):
    for x in range(len(board)):
        for y in range(len(board)):
            setAt(board, (x, y), randint(0, 1))

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

if __name__ == "__main__":
    print(nbrsnd((0, 0), 2))
    print(points_in_dimensions((2, 2, 3)))
