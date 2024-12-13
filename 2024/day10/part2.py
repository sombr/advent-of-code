#!/usr/bin/python3

import sys

def dfs(geo, r, c):
    trails = 0
    stack = [ (r, c) ]

    while stack:
        (r, c) = stack.pop()

        if geo[r][c] == 9:
            trails += 1

        for dr, dc in ( (-1,0), (1,0), (0,-1), (0,1) ):
            nr, nc = r+dr, c+dc
            if nr < 0 or nc < 0 or nr >= len(geo) or nc >= len(geo[0]):
                continue
            if geo[nr][nc] - geo[r][c] != 1:
                continue

            stack.append( (nr, nc) )

    return trails

def main():
    geo = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            geo.append([ int(x) for x in line.strip() ])

    trailheads = []
    for r in range(len(geo)):
        for c in range(len(geo[r])):
            if geo[r][c] == 0:
                trails  = dfs(geo, r, c)
                trailheads.append( trails )

    part2 = sum(trailheads)
    print(f"part2: {part2}")

main()
