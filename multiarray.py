from copy import deepcopy

def ndimensional(n, diameter, filler=None):
    lastlayer = [filler,]*diameter
    n -= 1
    while n > 0:
        for i in range(len(lastlayer)):
            lastlayer[i] = [deepcopy(lastlayer[i]) for _ in range(diameter)]
        n -= 1
    return lastlayer

if __name__ == "__main__":
    print(ndimensional(1, 3))
    print(ndimensional(2, 3))
    print(ndimensional(3, 3))
