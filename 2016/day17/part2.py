#!/usr/bin/python3

import os
import sys
import hashlib
from collections import deque

def solve():
    w = 4
    h = 4

    start = (0,0)

    seed = sys.argv[1]

    queue  = deque([ (start, "") ]) # pos, path so far
    moves = ( (0, -1, "U"), (0, 1, "D"), (-1, 0, "L"), (1, 0, "R") )

    longest_path = -1

    while queue:
        pos, path = queue.popleft()

        if pos == (w-1, h-1):
            if len(path) > longest_path:
                longest_path = len(path)
            continue

        hs = hashlib.md5( (seed + path).encode() ).hexdigest()[:4]
        is_open = [ not (h.isdigit() or h == "a") for h in hs ]
        candidates = [ m for m, f in zip( moves, is_open ) if f ]

        open_moves = []
        for dx, dy, dn in candidates:
            cx, cy = pos
            nx, ny = cx + dx, cy + dy

            if nx < 0 or ny < 0 or nx >= w or ny >= h:
                continue

            queue.append( ((nx, ny), path + dn) )

    return longest_path

def main():
    res = solve()

    print(res)

main()
