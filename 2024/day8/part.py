#!/usr/bin/python3

import sys

def show_state(state):
    return "\n".join(("".join(( str(e) for e in row )) for row in state))

def v_neg(a):
    (x, y) = a
    return (-x, -y)

def v_add(a, b):
    return (a[0]+b[0], a[1]+b[1])

def v_scale(a, s):
    return (a[0]*s, a[1]*s)

def v_is_in_bounds(x, y, bounds):
    (x0, y0, xm, ym) = bounds
    if x < x0 or y < y0 or x > xm or y > ym:
        return False
    return True

def main():
    state = []
    antistate1 = []
    antistate2 = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            row = list(line.strip())
            state.append( row )
            antistate1.append( [ e for e in row ] )
            antistate2.append( [ e for e in row ] )

    print(show_state(state))

    node_pos = {}
    for ridx, row in enumerate(state):
        for cidx, val in enumerate(row):
            if val != '.':
                node_pos[val] = node_pos.get(val, [])
                node_pos[val].append( (ridx, cidx) )

    bounds = (0, 0, len(state)-1, len(state[0])-1)
    
    anti_node_count1 = 0
    anti_node_count2 = 0
    for node, ps in node_pos.items():
        if len(ps) < 2:
            continue
        for f in range(len(ps)):
            for s in range(f+1, len(ps)):

                dv = v_add(ps[s], v_neg(ps[f]))
                rdv = v_neg(dv)

                for idx in range(1_000_000):
                    (r, c) = v_add( ps[s], v_scale( dv, idx ) )
                    if not v_is_in_bounds(r, c, bounds):
                        break
                    if idx == 1:
                        if antistate1[r][c] != '#':
                            anti_node_count1 += 1
                        antistate1[r][c] = '#'
                    if antistate2[r][c] != '#':
                        anti_node_count2 += 1
                    antistate2[r][c] = '#'

                for idx in range(1_000_000):
                    (r, c) = v_add( ps[f], v_scale( rdv, idx ) )
                    if not v_is_in_bounds(r, c, bounds):
                        break
                    if idx == 1:
                        if antistate1[r][c] != '#':
                            anti_node_count1 += 1
                        antistate1[r][c] = '#'
                    if antistate2[r][c] != '#':
                        anti_node_count2 += 1
                    antistate2[r][c] = '#'

    print("--- antinodes 1 ---")
    print(show_state(antistate1))

    print("--- antinodes 2 ---")
    print(show_state(antistate2))

    print(f">> part1 : {anti_node_count1}")
    print(f">> part2 : {anti_node_count2}")

main()
