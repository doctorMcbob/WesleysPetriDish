from pysrc.multiarray import ndimensional
from pysrc import automata

import traceback

dimensions = {}
cubes = {}

def add_pre_built(name, dim, cube):
    cubes[name] = cube
    dimensions[name] = dim
    return "Added cube {} from pre built".format(name)

def add_cube(name, n, dim, filler=0):
    cubes[name] = ndimensional(n, dim, filler=filler)
    dimensions[name] = dim
    return "Added new blank cube {}".format(name)

def build_cube(name, seed, length, rule):
    cube = []
    board = cubes[seed]
    buildfunction = automata.RULES[rule]
    while len(cube) < length:
        cube.append(board)
        try:
            board = buildfunction(board, dimensions[seed])
        except (IndexError, TypeError) as e:
            print(dimensions[seed])
            print(traceback.format_exc())
            return "Failed to build to cube {} with rule {} starting from cube {}".format(name, rule, seed)
    cubes[name] = cube
    dimensions[name] = tuple(
        [n for n in dimensions[seed]] + [len(cube)]
    )
    return "Built to cube {} with rule {} starting from cube {}".format(name, rule, seed)

def get_cube_names():
    return list(cubes.keys())

def get_cube(name):
    return cubes[name]

def get_cube_dimensions(name):
    return dimensions[name]

def make_slice(sliceto, slicefrom, idx):
    s = cubes[slicefrom][idx]
    if not type(s) == list: return "Cannot slice from 1 dimensional"
    cubes[sliceto] = s
    dimensions[sliceto] = dimensions[slicefrom][:-1]
    print(dimensions)
    return "Sliced {} at index {} to cube {}".format(slicefrom, idx, sliceto) 
