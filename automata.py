from multiarray import ndimensional

from utils import nbrs2d, nbrsnd, getAt, setAt, points_in_dimensions

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

def make_generic_ndimensional(name, n, ruleset, inverted=False):
    def rule(board, dimensions):
        new = ndimensional(n, dimensions, filler=0)
        for pos in points_in_dimensions(dimensions):
            serilized_state = ""
            for nbr in nbrsnd(pos, n):
                at = getAt(board, nbr)
                if at is None: at=0
                serilized_state += str(at)
            output = 1 if inverted else 0
            for rule_segment in RULE_SETS[name]:
                if generic_check_against(state, rule_segment):
                    output = 1 if inverted else 0
                    break
            setAt(new, pos, output)
        return new
    return rule
                
def generic_check_against(state, rule_segment):
    for idx in range(len(state)):
        slot = state[idx]
        check = rule_segment[idx]
        if slot != check and check != "?":
            return False
    return True

RULES = {
    "life": life2d,
}

RULE_SETS = {}
