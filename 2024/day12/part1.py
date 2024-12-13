#!/usr/bin/python3

import sys

def dfs(state, r, c, visited):
    if (r,c) in visited:
        return None, None

    area = 0
    perimeter = 0

    queue = [ (r,c) ]
    while queue:
        cr, cc = queue.pop()

        if (cr, cc) in visited:
            continue

        visited.add( (cr,cc) )
        area += 1
        perimeter += 4

        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                if dr != 0 and dc != 0:
                    continue
                
                nr, nc = cr + dr, cc + dc

                if nr < 0 or nc < 0 or nr >= len(state) or nc >= len(state[0]):
                    continue
                if state[nr][nc] != state[cr][cc]:
                    continue

                if (nr, nc) in visited:
                    perimeter -= 2
                else:
                    queue.append( (nr, nc) )

    return (area, perimeter)


def main():
    state = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            state.append( list(line.strip()) )

    total_price = 0
    visited = set()
    for r in range(len(state)):
        for c in range(len(state[0])):
            area, perimeter = dfs(state, r, c, visited)
            if area is None:
                continue

            print(f">>> ({r},{c}) {state[r][c]} - {area} {perimeter}")
            total_price += area * perimeter

    print(f">>> part 1: {total_price}")

main()
