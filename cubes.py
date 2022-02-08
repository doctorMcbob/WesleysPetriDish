from multiarray import ndimensional
# dimensions does not include index dimension
dimensions = {}
cubes = {}

def add_pre_built(name, dim, cube):
    cubes[name] = cube
    dimensions[name] = dim

def add_cube(name, n, dim, filler=None):
    cubes[name] = ndimensional(n, dim, filler=filler)
    dimensions[name] = dim

def build_cube(name, seed, length, buildfunction):
    cube = []
    board = cubes[seed]
    while len(cube) < length:
        cube.append(board)
        board = buildfunction(board, dimensions[name])
    cubes[name] = cube

def get_cube_names():
    return list(cubes.keys())

def get_cube(name):
    return cubes[name]

def get_cube_dimensions(name):
    return dimensions[cube]
