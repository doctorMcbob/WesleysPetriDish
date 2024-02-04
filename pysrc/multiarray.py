from copy import deepcopy

def ndimensional(n, dimensions, filler=None):
    i = 0 #len(dimensions)-1

    lastlayer = [filler,] * dimensions[i]
    while i < len(dimensions)-1:#i > 0:
        i +=1 #-= 1
        copy = deepcopy(lastlayer)
        lastlayer = [deepcopy(copy) for _ in range(dimensions[i])]
    return lastlayer

