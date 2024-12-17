#!/usr/bin/python3

import sys
import math
from collections import deque

ROTATIONS = (
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0)
)

def print_rows(field, sep = ""):
    for row in field:
        for val in row:
            print(str(val), end=sep)
        print()

def bfs(field, start_pos, start_rotation, end):
    queue = deque([ (start_pos, start_rotation, 0, set()) ])
    #                position   rotation East cost path

    final_costs = []
    final_paths = {}

    visited = {}
    while queue:
        pos, rot, cost, path = queue.popleft()

        if visited.get( (pos, rot), math.inf ) <= cost:
            continue

        path.add(pos)
        if pos == end:
            final_costs.append(cost)
            final_paths[cost] = final_paths.get(cost, [])
            final_paths[cost].append( path )
            continue

        visited[(pos,rot)] = cost

        for drotation in range(len(ROTATIONS)):
            idx = (rot + drotation) % len(ROTATIONS)
            rotation_cost = 0
            if drotation == 1 or drotation == 3:
                rotation_cost = 1000
            if drotation == 2:
                rotation_cost = 2000

            move_cost = cost + rotation_cost + 1

            cr, cc = pos
            dr, dc = ROTATIONS[idx]

            nr, nc = cr+dr, cc+dc

            if nr < 0 or nc < 0 or nr >= len(field) or nc >= len(field[0]):
                continue
            if field[nr][nc] == "#":
                continue
            if visited.get( ((nr, nc), idx), math.inf ) <= move_cost:
                continue

            queue.append( ( (nr,nc), idx, move_cost, set(path)) )

    best_cost = min(final_costs, default=math.inf)
    best_paths = final_paths.get(best_cost, set())

    return (best_cost, best_paths)

def main():
    field = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            field.append( list(line.strip()) )

    print_rows(field)

    S = ()
    E = ()

    for ridx, row in enumerate(field):
        for cidx, val in enumerate(row):
            if val == "S":
                S = (ridx, cidx)
            if val == "E":
                E = (ridx, cidx)

    cost, paths = bfs(field, S, 0, E)
    print(">>> part1 cost:", cost)

    best_seats = paths[0]
    for alternative in paths:
        best_seats = best_seats & alternative

    print(">>> part2 seats: ", len(best_seats))

main()
