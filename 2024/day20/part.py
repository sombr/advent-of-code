#!/usr/bin/pypy3

import sys
from collections import deque

def load_map(filename):
    m = []
    with open(filename, "r") as file:
        for line in file:
            m.append(line.strip())

    return tuple(m)

def find_path(m, start, end):
    visited = set()

    r, c = start
    q = deque([ (r,c,[(r,c)]) ])
    while q:
        r, c, path = q.popleft()

        if (r,c) == end:
            return path

        if (r,c) in visited:
            continue

        visited.add( (r,c) )

        for dr, dc in ( (0,1), (0,-1), (1,0), (-1,0) ):
            nr, nc = r+dr, c+dc

            if nr < 0 or nc < 0 or nr >= len(m) or nc >= len(m[0]):
                continue
            if (nr, nc) in visited:
                continue
            if m[nr][nc] == "#":
                continue

            new_path = path + [ (nr, nc) ]
            q.append( (nr,nc,new_path) )
    return None

def find_jumps(path, dist):
    pcost = {}

    for idx, pos in enumerate(path):
        pcost[pos] = idx

    jumps = {}
    for pos, step in pcost.items():
        r, c = pos
        # 1 2 3 4
        #     # 5
        # 9 8 7 6

        for dr in range(-dist, dist+1):
            cspan = dist - abs(dr)
            for dc in range(-cspan, cspan+1):
                nr, nc = r+dr, c+dc

                path_span = abs(dr) + abs(dc)

                next_step = pcost.get( (nr,nc), 0 )
                if next_step - path_span <= step:
                    continue

                saving = (next_step - step) - path_span

                if saving > 0:
                    jumps[ ((r,c), (nr,nc)) ] = saving

    return jumps

def print_path(m, path):
    for ridx, row in enumerate(m):
        for cidx, val in enumerate(row):
            if val in ["S", "E"]:
                print(val, end="")
            elif (ridx, cidx) in path:
                print("*", end="")
            else:
                print(val, end="")
        print()

def main():
    m = load_map(sys.argv[1])

    # find start and end
    S = ()
    E = ()
    for ridx, row in enumerate(m):
        for cidx, val in enumerate(row):
            if val == "S":
                S = (ridx, cidx)
            elif val == "E":
                E = (ridx, cidx)

    print(f"start: {S} end: {E}")

    path = find_path(m, S, E)
    jumps = find_jumps(path, 2)

    part1 = 0
    for saving in jumps.values():
        if saving >= 100:
            part1 += 1

    print("part1 >> ", part1)

    # part2
    jumps = find_jumps(path, 20)
    part2 = 0
    for saving in jumps.values():
        if saving >= 100:
            part2 += 1

    print("part2 >> ", part2)

main()
