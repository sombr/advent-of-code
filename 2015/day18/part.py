#!/usr/bin/python3

import sys
import numpy as np

def count_neighbours(state, r, c):
    res = 0
    for dr in [-1,0,1]:
        for dc in [-1,0,1]:
            if dr == 0 and dc == 0:
                continue
            rn = r + dr
            cn = c + dc

            if rn < 0 or cn < 0:
                continue
            if rn >= state.shape[0] or cn >= state.shape[1]:
                continue

            res += state[rn, cn]

    return res

def main():
    state = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            lights = [ 1 if l == "#" else 0 for l in line.strip() ]
            state.append(lights)

    state = np.array(state, dtype=np.uint8)
    for step in range(100):
        next_state = np.zeros_like(state, dtype=np.uint8)
        for r in range(state.shape[0]):
            for c in range(state.shape[1]):
                neighbours_on = count_neighbours(state, r, c)

                if state[r, c] > 0:
                    if neighbours_on == 2 or neighbours_on == 3:
                        next_state[r, c] = 1
                    else:
                        next_state[r, c] = 0
                else:
                    if neighbours_on == 3:
                        next_state[r, c] = 1
                    else:
                        next_state[r, c] = 0
        state = next_state

    print(f"part 1 >> {np.sum(state)}")

main()