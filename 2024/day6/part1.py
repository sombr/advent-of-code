#!/usr/bin/python3

import sys
import numpy as np

DIRECTION = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]

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
    
    state = np.asarray(state)
    return guard, state

def make_step(guard, state):
    next_guard = None
    direction, gr, gc = guard

    dr, dc = DIRECTION[direction]
    nr, nc = gr+dr, gc+dc

    if nr < 0 or nc < 0 or nr >= state.shape[0] or nc >= state.shape[1]:
        return next_guard
    
    if state[nr, nc] >= 0:
        state[nr, nc] = 1
        next_guard = (direction, nr, nc)
    else:
        ndir = (direction + 1) % len(DIRECTION)
        next_guard = (ndir, gr, gc)
        
    return next_guard

def main():
    guard, state = load_state(sys.argv[1])

    print(guard)
    print(state)

    while True:
        new_guard = make_step(guard, state)
        if new_guard is None:
            break

        guard = new_guard

    print("end state:")
    print(state)

    path_sum = np.sum(np.clip(state, 0, 1))
    print(">>> part1: ", path_sum)

main()