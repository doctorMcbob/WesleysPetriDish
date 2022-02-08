from random import randint

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

