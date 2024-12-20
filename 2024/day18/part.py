#!/usr/bin/python3

import sys
from collections import deque

def get_state_after(steps, walls):
    return set( walls[:steps] )

def bfs(state, size):
    visited = set()

    q = deque([ (0,0,0) ])
    while q:
        x, y, steps = q.popleft()

        if x == size and y == size:
            return steps

        if (x,y) in visited:
            continue

        visited.add( (x,y) )

        for dx, dy in ( (0,1), (0,-1), (1,0), (-1,0) ):
            nx, ny = x+dx, y+dy

            if (nx, ny) in visited:
                continue
            if (nx, ny) in state: # blocked
                continue
            if nx < 0 or ny < 0 or ny > size or nx > size:
                continue

            q.append( (nx,ny,steps+1) )

    return -1


def main():
    walls = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            x, y = ( int(x) for x in line.strip().split(",") )
            walls.append( (x, y) )

    state = get_state_after(1024, walls)
    steps = bfs(state, 70)
    
    print("part1 >> ", steps)

    for falls in range(len(walls)):
        state = get_state_after(falls, walls)
        if bfs(state, 70) < 0:
            print("part2 >> ", walls[falls-1])
            break

main()
