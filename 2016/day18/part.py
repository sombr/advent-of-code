#!/usr/bin/python3

import sys

def solve(seed, rows):
    row = list(seed)
    safe_tiles = 0
    for ridx in range(rows):
        for tile in row:
            if tile == ".":
                safe_tiles += 1
        row = compute_row(row)

    print(f"safe tiles: {safe_tiles}")


def compute_row(prev):
    row = []
    tiles = len(prev)

    for idx in range(tiles):
        left_safe = idx == 0 or prev[idx-1] == "."
        right_safe = idx == (tiles-1) or prev[idx+1] == "."

        this_trap = left_safe ^ right_safe
        row.append( "^" if this_trap else "." )

    return row

solve(sys.argv[1], int(sys.argv[2]))
