#!/usr/bin/python3

import sys
from collections import deque

SHOW_STEPS = False

def show_state(state, min_floor, max_floor):
    disp = [ [ '__' for _ in range(len(state)) ] for _ in range(max_floor-min_floor+1) ]

    for idx, (item, floor) in enumerate(state):
        disp[ max_floor - floor ][idx] = item

    return "\n".join([ " ".join(row) for row in disp ])

def encode_state(items):
    return tuple( sorted(items.items(), key=lambda x: x[0]) )

def is_safe_state(state):
    chips = {}
    floor2gen = {}

    for tag, floor in state:
        if tag == " E":
            continue

        if tag[1] == "G": # generator
            floor2gen[floor] = floor2gen.get(floor, set())
            floor2gen[floor].add( tag[0] )
        else:
            chips[tag[0]] = floor

    for chip, floor in chips.items():
        colocated_gens = floor2gen.get(floor, set())
        if len(colocated_gens) > 0 and chip not in colocated_gens:
            return False

    return True

def get_safe_moves_from_state(state, min_floor, max_floor):
    items = dict(state)

    elevator_level = items[' E']
    items_on_elevator_level = [
        item for item, floor in items.items() if floor == elevator_level and item != ' E'
    ]

    moves = []
    for first in items_on_elevator_level:
        for second in ([None] + items_on_elevator_level):
            for direction in [-1, 1]:
                if elevator_level == min_floor and direction == -1:
                    continue
                if elevator_level == max_floor and direction == 1:
                    continue
                if first == second:
                    continue

                load = [ x for x in [' E', first, second] if x is not None ]

                for l in load:
                    items[l] += direction
                state = encode_state(items)
                for l in load:
                    items[l] -= direction

                if is_safe_state(state):
                    moves.append(state)
    return moves

def is_final(state, max_floor):
    return len([ floor for (_, floor) in state if floor < max_floor ]) == 0

def bfs(start_state, min_floor, max_floor):
    queue = deque([ (0, start_state) ])

    visited = set()
    while queue:
        cur_steps, cur_state = queue.popleft()

        if SHOW_STEPS:
            print(f"\n\n ---- {cur_steps} ---- ")
            print(show_state(cur_state, min_floor, max_floor))

        if is_final(cur_state, max_floor):
            return cur_steps

        if cur_state in visited:
            continue
        visited.add(cur_state)

        safe_moves = get_safe_moves_from_state( cur_state, min_floor, max_floor )
        for move in safe_moves:
            if move in visited:
                continue
            queue.append( (cur_steps+1, move) )

    return None

def main():
    items = { ' E': 1 }
    min_floor = 1_000_000
    max_floor = -1_000_000
    with open(sys.argv[1], "r") as file:
        for line in file:
            floor, content = ( x.strip() for x in line.split(":") )
    
            floor = int(floor[1:])
            content = content.split()

            min_floor = min(min_floor, floor)
            max_floor = max(max_floor, floor)

            for item in content:
                items[item] = floor


    min_steps = bfs( encode_state(items), min_floor, max_floor )
    print(f"part1 >> {min_steps}")

main()
