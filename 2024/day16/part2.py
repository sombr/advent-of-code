#!/usr/bin/python3

import sys
import heapq
import numpy as np

RD = {
    ">": (0,1),
    "<": (0,-1),
    "^": (-1,0),
    "v": (1,0)
}

RO = ">^<v"
OR = {
    ">": 0,
    "^": 1,
    "<": 2,
    "v": 3
}

def print_map_with_path(m, path):
    pos2a = dict( (  ((r,c),a) for r,c,a in path ) )
    for r in range(m.shape[0]):
        for c in range(m.shape[1]):
            if m[r,c] in ("S", "E", "#"):
                print(m[r,c], end="")
            elif (r,c) in pos2a:
                print(RO[pos2a[(r,c)]], end="")
            else:
                print(m[r,c], end="")
        print()

def load_map(filename):
    m = []
    with open(filename, "r") as file:
        for line in file:
            m.append(list(line.strip()))

    return np.asarray(m)

def dijsktra(m, r, c):
    state_shape = ( m.shape[0], m.shape[1], 4 )

    dist = np.zeros( state_shape ) + np.inf
    prev = [ [ [ None for _ in range(4) ] for _ in range(m.shape[1]) ] for _ in range(m.shape[0]) ]

    dist[r,c,0] = 0

    q = [ (0, r, c, 0) ]
    while q:
        cost, r, c, a = heapq.heappop(q)

        if cost > dist[ r, c, a ]:
            continue

        for da in range(0,4):
            rotation_cost = 0
            if da == 1 or da == 3:
                rotation_cost = 1000
            if da == 2:
                rotation_cost = 2000

            na = (a + da) % 4
            dr, dc = RD[ RO[ na ] ]
            nr, nc = r+dr, c+dc

            if nr < 0 or nr >= m.shape[0] or nc < 0 or nc >= m.shape[1]:
                continue
            if m[nr, nc] == "#":
                continue

            move_cost = rotation_cost + 1
            path_cost = cost + move_cost
            if path_cost < dist[ nr, nc, na ]:
                dist[ nr, nc, na ] = path_cost
                prev[ nr ][ nc ][ na ] = set([ (r, c, a, cost) ])

                heapq.heappush(q, ( path_cost, nr, nc, na ))
            elif path_cost == dist[ nr, nc, na ]:
                prev[ nr ][ nc ][ na ].add( (r,c,a,cost) )

    return dist, prev


def trace_path(prev, r, c, a):
    if prev[r][c][a] is None:
        return [ [ (r,c,a) ] ]
    else:
        extended_paths = []
        for branch in prev[r][c][a]:
            pr, pc, pa, _ = branch

            for path in trace_path(prev, pr, pc, pa):
                pp = [ (r,c,a) ] + path
                extended_paths.append(pp)

        return extended_paths

def main():
    m = load_map(sys.argv[1])

    S = np.argwhere(m == "S")[0]
    E = np.argwhere(m == "E")[0]

    dist, prev = dijsktra(m, S[0], S[1])

    end_dist = dist[ E[0], E[1] ]
    best_cost = int(min(end_dist))
    print(f">>> best_cost (part1): {best_cost}")

    approaches = []
    for idx, dist in enumerate(end_dist):
        if dist < np.inf and int(dist) == best_cost:
            approaches.extend( prev[ E[0] ][ E[1] ][idx] )

    print(approaches)

    paths = []
    for approach in approaches:
        r, c, a, _ = approach
        p = trace_path(prev, r, c, a)
        paths.extend(p)

    if False:
        print(paths)
        for path in paths:
            print("---")
            print_map_with_path(m, path)

    alltiles = set()
    for path in paths:
        for tile in path:
            r, c, a = tile
            alltiles.add( (r,c) )

    print("part2 >>> ", len(alltiles)+1)

main()
