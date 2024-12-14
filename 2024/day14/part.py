#!/usr/bin/python3

import sys

def print_robots(robots, xsize, ysize):
    field = [ [ 0 for _ in range(xsize)  ] for _ in range(ysize) ]

    for (x, y) in robots:
        field[y][x] += 1

    for r in range(len(field)):
        for c in range(len(field[r])):
            field[r][c] = "·" if field[r][c] == 0 else str(field[r][c])
            #field[r][c] = " " if field[r][c] == 0 else str(field[r][c])

    print("\n".join( ( "".join(row) for row in field ) ))

def simulate_robot(robot, xsize, ysize, t):
    (x, y), (dX, dY) = robot

    for _ in range(t):
        x += dX
        y += dY

        if x < 0:
            x += xsize
        if y < 0:
            y += ysize

        x = x % xsize
        y = y % ysize

    return (x,y)

def main():
    robots = []
    with open(sys.argv[1], "r") as file:
        for line in file.read().splitlines():
            pos, vel = ( tuple( ( int(c) for c in p.split("=")[-1].split(",") ) ) for p in line.split() )
            robots.append( (pos, vel) )

    
    print(robots)

    XS = 101
    YS = 103

    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0

    positions = []
    for r in robots:
        x, y = simulate_robot(r, XS, YS, 100)
        positions.append( (x,y) )

        if x < XS // 2 and y < YS // 2:
            q1 += 1
        elif x > XS // 2 and y < YS // 2:
            q2 += 1
        elif x > XS // 2 and y > YS // 2:
            q3 += 1
        elif x < XS // 2 and y > YS // 2:
            q4 += 1

    print_robots(positions, XS, YS)

    print(f"part1 >> {q1*q2*q3*q4}")

    bstate = set(robots)
    for t in range(1, 1_000_000):
        positions = []
        new_state = []
        for r in robots:
            x, y = simulate_robot(r, XS, YS, t)
            positions.append( (x,y) )
            new_state.append( ((x,y), r[1]) )

        if (t - 124) % 101 == 0:
            print(f" ----- TIME: {t} -----")
            print_robots(positions, XS, YS)

        if set(new_state) == bstate:
            break

main()
