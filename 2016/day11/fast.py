#!/usr/bin/python3

import sys
from collections import deque

FMIN = 0
FMAX = 3

SHOW_STEPS = False

def load_initial_state(filename):
    items = { ' E': 0 }
    with open(filename, "r") as file:
        for line in file:
            floor, content = ( x.strip() for x in line.split(":") )
            if floor == "E":
                items[" E"] = int(content)
                continue
    
            floor = int(floor[1:])
            content = content.split()

            for item in content:
                items[item] = floor

    types = (len(items) - 1) // 2
    type_rev_order = sorted(set( ( t[0] for t in items.keys() if t[0] != " " ) ))
    type_order = dict([(t, idx) for idx, t in enumerate(type_rev_order)])

    gen_levels = [-1, 0, 0, 0, 0]
    chip_levels = [-1, 0, 0, 0, 0]

    elevator_level = 1
    for item, lvl in items.items():
        if item == " E":
            elevator_level = lvl
            continue
        if item[1] == "G":
            offset = type_order[ item[0] ]
            lvlmap = gen_levels[ lvl ]
            lvlmap = lvlmap | (1 << offset)
            gen_levels[ lvl ] = lvlmap
        elif item[1] == "M":
            offset = type_order[ item[0] ]
            lvlmap = chip_levels[ lvl ]
            lvlmap = lvlmap | (1 << offset)
            chip_levels[ lvl ] = lvlmap
        else:
            raise RuntimeError(":(")

    state = (elevator_level, tuple( gen_levels[1:] ), tuple( chip_levels[1:] ))
    return state, type_rev_order

def print_state(state, types):
    e, gens, chips = state

    for lvl in range(3, -1, -1):
        if e == lvl:
            print("_E", end = "")
        else:
            print("__", end = "")

        for offset, t in enumerate(types):
            g_present = (gens[lvl] & (1 << offset)) != 0
            c_present = (chips[lvl] & (1 << offset)) != 0

            print(" ", end = "")

            if g_present:
                print(f"{t}G", end = "")
            else:
                print("__", end = "")

            if c_present:
                print(f"{t}M", end = "")
            else:
                print("__", end = "")

        print()

def is_safe_level(gsl, csl):
    delta = gsl ^ csl
    delta_chip = delta & csl
    return gsl == 0 or csl == 0 or gsl == csl or delta_chip == 0

def is_safe_state(state):
    _, gs, cs = state

    for lvl in range(4):
        if is_safe_level(gs[lvl], cs[lvl]):
            continue
        return False

    return True

def move_item(from_lvl, to_lvl, offset):
    mask = 1 << offset
    assert(from_lvl & mask != to_lvl & mask)

    from_lvl = from_lvl ^ (1 << offset)
    to_lvl = to_lvl ^ (1 << offset)

    return from_lvl, to_lvl

def move_item_with_type(from_gs, to_gs, from_cs, to_cs, offset, is_gen):
    n_from_gs = from_gs
    n_to_gs = to_gs
    n_from_cs = from_cs
    n_to_cs = to_cs

    if is_gen:
        n_from_gs, n_to_gs = move_item(from_gs, to_gs, offset)
    else:
        n_from_cs, n_to_cs = move_item(from_cs, to_cs, offset)

    return (n_from_gs, n_to_gs, n_from_cs, n_to_cs)

def move_between_levels(gs, cs, from_lvl, to_lvl, offset, is_gen):
    (n_from_gs, n_to_gs, n_from_cs, n_to_cs) = move_item_with_type(
            gs[from_lvl], gs[to_lvl], cs[from_lvl], cs[to_lvl],
            offset, is_gen)

    n_gs = [ x for x in gs ]
    n_cs = [ x for x in cs ]

    n_gs[from_lvl] = n_from_gs
    n_gs[to_lvl] = n_to_gs
    n_cs[from_lvl] = n_from_cs
    n_cs[to_lvl] = n_to_cs

    return (tuple(n_gs), tuple(n_cs))

def get_safe_moves_from_state(state, types):
    el, gs, cs = state

    moves = []

    span = len(types)
    for direction in (-1,1):
        nel = el + direction
        if nel < FMIN:
            continue
        elif nel > FMAX:
            continue

        for first in range(span*2):
            is_gen = first < span
            first_mask = 1 << (first % span)
            first_present = (gs[el] if is_gen else cs[el]) & first_mask

            if first_present == 0:
                continue

            # try one
            ngs, ncs = move_between_levels(gs, cs, el, nel, first % span, is_gen)
            will_current_be_safe = is_safe_level(ngs[el], ncs[el])
            will_new_be_safe = is_safe_level(ngs[nel], ncs[nel])
            if will_current_be_safe and will_new_be_safe:
                moves.append( (nel, ngs, ncs) )
            elif not will_new_be_safe:
                continue
            
            for second in range(first+1, span*2):
                is_second_gen = second < span
                second_mask = 1 << (second % span)
                second_present = (gs[el] if is_second_gen else cs[el]) & second_mask

                if second_present == 0:
                    continue

                sngs, sncs = move_between_levels(ngs, ncs, el, nel, second % span, is_second_gen)
                if is_safe_level(sngs[el], sncs[el]) and is_safe_level(sngs[nel], sncs[nel]):
                    moves.append( (nel, sngs, sncs) )

    return moves

def is_final(state, types):
    mask = (1 << (len(types))) - 1
    return state[1][FMAX] == mask and state[2][FMAX] == mask

def bfs(start_state, types):
    queue = deque([ (0, start_state) ])

    visited = set()
    while queue:
        cur_steps, cur_state = queue.popleft()

        if SHOW_STEPS:
            print(f"\n\n ---- {cur_steps} ---- ")
            print_state(cur_state, types)

        if is_final(cur_state, types):
            return cur_steps

        if cur_state in visited:
            continue
        visited.add(cur_state)

        safe_moves = get_safe_moves_from_state( cur_state, types )
        for move in safe_moves:
            if move in visited:
                continue
            queue.append( (cur_steps+1, move) )

    return None

def main():
    state, types = load_initial_state(sys.argv[1])

    steps = bfs(state, types)
    print(f">>> steps {steps}")

main()
