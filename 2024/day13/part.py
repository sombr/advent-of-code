#!/usr/bin/python3

import sys

def parse_line(line, sep):
    _, coords = line.split(": ")
    coords = ( int(cs.split(sep).pop()) for cs in coords.split(", ") )

    return tuple(coords)

def parse_block(block):
    lines = block.splitlines()
    assert(len(lines) == 3)

    la, lb, lt = lines

    amove = parse_line(la, "+")
    bmove = parse_line(lb, "+")
    target = parse_line(lt, "=")

    return (amove, bmove, target)

def find_solution(machine):
    # Xa*n + Xb*m = Xtarget
    # Ya*n + Yb*m = Ytarget
    #
    # 2:-> n = (Ytarget - Yb*m) / Ya
    # 1:-> (Ytarget - Yb*m) * Xa / Ya + Xb*m = Xtarget
    # (Ytarget - Yb*m)*Xa + Ya*Xb*m = Ya*Xtarget
    # Ytarget*Xa - Xa*Yb*m + Xb*Ya*m = Xtarget*Ya
    # (Xb*Ya - Xa*Yb)*m = Xtarget*Ya - Xa*Ytarget
    # m = (Xtarget*Ya - Xa*Ytarget) / (Xb*Ya - Xa*Yb)
    # n = (2)

    (Xa, Ya), (Xb, Yb), (Xt, Yt) = machine

    m = (Xt*Ya - Xa*Yt) / (Xb*Ya - Xa*Yb)
    n = (Yt - Yb*m) / Ya

    if m % 1 == 0 and n % 1 == 0:
        cost = int(3*n + m)
        return (cost, int(n), int(m))

    return (None, None, None)

def main():
    blocks = []
    with open(sys.argv[1], "r") as file:
        blocks = file.read().split("\n\n")

    machines = tuple( (parse_block(b) for b in blocks) )

    solutions_cost = 0
    for m in machines:
        cost, a, b = find_solution(m)
        if cost is None:
            continue
        solutions_cost += cost

    print(f"part1 >> {solutions_cost}")

    span = 10000000000000
    p2machines = []
    for m in machines:
        a, b, (Xt, Yt) = m
        p2machines.append( (a,b,(Xt+span, Yt+span)) )

    solutions_cost = 0
    for m in p2machines:
        cost, a, b = find_solution(m)
        if cost is None:
            continue
        solutions_cost += cost

    print(f"part2 >> {solutions_cost}")

main()
