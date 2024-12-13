#!/usr/bin/python3

import sys

def print_cells(cells, size, inside = {}):
    min_row = min(cells, key=lambda x: x[0], default=(0,0))[0] - 1
    max_row = max(cells, key=lambda x: x[0], default=(size,0))[0] + 1

    min_col = min(cells, key=lambda x: x[1], default=(0,0))[1] - 1
    max_col = max(cells, key=lambda x: x[1], default=(0,size))[1] + 1

    rows = []
    for r in range(min_row, max_row+1):
        row = []
        for c in range(min_col, max_col+1):
            if (r,c) in inside:
                row.append( '#' )
            else:
                row.append( str(cells.get((r,c), '·')) )
        rows.append(row)
    print("\n".join( ( "".join(r) for r in  rows ) ))

def count_sides(edges, tag, cells):
    visited = {}

    sides = 0
    for start_cell in sorted(edges.keys()):
        print(f"--- start cell {start_cell} --- sides {sides} --- ")
        if visited.get(start_cell, 0) >= edges[start_cell]:
            continue

        explored_v = False
        explored_h = False
        while visited.get(start_cell, 0) < edges[start_cell]:
            # select direction
            (cr, cc) = start_cell

            if not explored_v:
                # vertical
                nr = cr+1
                while visited.get( (nr, cc), 0) < edges.get( (nr, cc), 0 ):
                    visited[ (nr, cc) ] = visited.get( (nr, cc), 0 ) + 1
                    nr += 1
                nr = cr-1
                while visited.get( (nr, cc), 0) < edges.get( (nr, cc), 0 ):
                    visited[ (nr, cc) ] = visited.get( (nr, cc), 0 ) + 1
                    nr -= 1
                explored_v = True

            if not explored_h:
                # horizontal
                nc = cc+1
                while visited.get( (cr, nc), 0 ) < edges.get( (cr, nc), 0 ):
                    visited[ (cr, nc) ] = visited.get( (cr, nc), 0 ) + 1
                    nc += 1
                nc = cc-1
                while visited.get( (cr, nc), 0 ) < edges.get( (cr, nc), 0 ):
                    visited[ (cr, nc) ] = visited.get( (cr, nc), 0 ) + 1
                    nc -= 1
                explored_h = True

            visited[start_cell] = visited.get(start_cell, 0 ) + 1
            sides += 1

            print_cells(visited, 10, cells)
            print(f"found side, now: {sides}")

    return sides

def find_edges(cells):
    cells = set(cells)
    edges = {}
    for (cr, cc) in cells:
        for (dr, dc) in ( (0,1), (0,-1), (1,0), (-1,0) ):
            nr, nc = cr + dr, cc + dc

            if (nr, nc) in cells:
                continue

            edges[ (nr, nc) ] = edges.get( (nr, nc), 0 ) + 1

    return edges

def dfs(state, r, c, visited):
    if (r,c) in visited:
        return None, None

    area = 0

    cells = []
    queue = [ (r,c) ]
    while queue:
        cr, cc  = queue.pop()

        if (cr, cc) in visited:
            continue

        visited.add( (cr,cc) )
        area += 1

        cells.append( (cr,cc) )

        for (dr, dc) in ( (0,1), (0,-1), (1,0), (-1,0) ):
            nr, nc = cr + dr, cc + dc

            if nr < 0 or nc < 0 or nr >= len(state) or nc >= len(state[0]):
                continue
            if state[nr][nc] != state[cr][cc]:
                continue

            if (nr, nc) in visited:
                pass
            else:
                queue.append( (nr, nc) )

    return (area, cells)


def main():
    state = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            state.append( list(line.strip()) )

    total_price = 0
    visited = set()
    for r in range(len(state)):
        for c in range(len(state[0])):
            area, cells = dfs(state, r, c, visited)
            if area is None:
                continue

            tag = state[r][c]

            edges = find_edges(cells)

            print("111: sides")
            print_cells(edges, 10, cells)

            sides = count_sides(edges, tag, cells)
            print(f"{tag} : {area} x {sides} = {area*sides}")
            if tag == "B" and area == 23:
                print("--------------------------")
                print_cells(edges, 10, cells)
                print("--------------------------")

            total_price += area*sides

    print(f">>> part 2: {total_price}")

main()
