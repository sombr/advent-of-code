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

    while queue:
        pos, path = queue.popleft()

        if pos == (w-1, h-1):
            return path

        hs = hashlib.md5( (seed + path).encode() ).hexdigest()[:4]
        is_open = [ not (h.isdigit() or h == "a") for h in hs ]
        candidates = [ m for m, f in zip( moves, is_open ) if f ]

        for dx, dy, dn in candidates:
            cx, cy = pos
            nx, ny = cx + dx, cy + dy

            if nx < 0 or ny < 0 or nx >= w or ny >= h:
                continue

            queue.append( ((nx, ny), path + dn) )

    return None

def main():
    res = solve()

    print(res)

main()
