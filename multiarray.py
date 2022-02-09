from copy import deepcopy

def ndimensional(n, dimensions, filler=None):
    dimensions = dimensions[::-1]
    n -= 1
    lastlayer = [filler,] * dimensions[n]
    while n > 0:
        n -= 1
        for i in range(len(lastlayer)):
            lastlayer[i] = [deepcopy(lastlayer[i]) for _ in range(dimensions[n])]
    return lastlayer

