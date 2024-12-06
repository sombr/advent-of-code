#!/usr/bin/python3

import sys

DIRECTION = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]

DIRLEN = len(DIRECTION)

def load_state(filename):
    guard = None
    state = []

    with open(filename, "r") as file:
        for ridx, line in enumerate(file):
            line = line.strip()

            row = []
            for cidx, pos in enumerate(line):
                e = 0
                match pos:
                    case ".":
                        e = 0
                    case "#":
                        e = -1
                    case "^":
                        e = 1
                        guard = (0, ridx, cidx)
                row.append(e)
            state.append(row)
    
    return guard, state

def run_sim(guard, state, rows, cols, track_points = True):
    positions = set([ guard ])
    points = set()

    is_loop = False
    while True:
        new_guard = make_step(guard, state, rows, cols)
        if new_guard is None:
            break

        guard = new_guard

        if guard in positions:
            is_loop = True
            break

        positions.add(guard)

        if track_points:
            _, gr, gc = guard
            points.add( (gr, gc) )

    return is_loop, points


def make_step(guard, state, rows, cols):
    next_guard = None
    direction, gr, gc = guard

    dr, dc = DIRECTION[direction]
    nr, nc = gr+dr, gc+dc

    if nr < 0 or nc < 0 or nr >= rows or nc >= cols:
        return next_guard
    
    if state[nr][nc] >= 0:
        state[nr][nc] = 1
        next_guard = (direction, nr, nc)
    else:
        ndir = (direction + 1) % DIRLEN
        next_guard = (ndir, gr, gc)
        
    return next_guard

def main():
    guard, state = load_state(sys.argv[1])
    rows, cols = len(state), len(state[0])
    is_loop, candidates = run_sim(guard, state, rows, cols)

    succussful_loops = 0
    for cr, cc in candidates:
        state[cr][cc] = -1
        now_loop, _ = run_sim(guard, state, rows, cols, track_points = False)
        state[cr][cc] = 0

        if now_loop:
            succussful_loops += 1

    print("part2 >> ", succussful_loops)

main()
