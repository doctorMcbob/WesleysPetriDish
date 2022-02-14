from copy import deepcopy

def ndimensional(n, dimensions, filler=None):
    i = 0
    lastlayer = [filler,] * dimensions[i]
    while n-1 > i:
        i += 1
        for idx in range(len(lastlayer)):
            lastlayer[idx] = [deepcopy(lastlayer[idx]) for _ in range(dimensions[i])]
    return lastlayer

