#!/usr/bin/python3

import sys

def check_if_safe(r):
    order = (r[-1] - r[0])
    order = 0 if order == 0 else order // abs(order)
    
    if order == 0:
        return False

    is_safe = True
    for idx in range(1, len(r)):
        delta = r[idx] - r[idx-1]
        delta_sign = 0 if delta == 0 else delta // abs(delta)

        if delta_sign != order:
            is_safe = False
            break
        if abs(delta) < 1 or abs(delta) > 3:
            is_safe = False
            break

    return is_safe

def main():
    reports = []
    with open(sys.argv[1], "r") as file:
        reports = [ [ int(r) for r in l.strip().split() ] for l in file.readlines() ]

    safe = 0
    safe2 = 0
    for r in reports:
        is_safe = check_if_safe(r)
        if is_safe:
            safe += 1
            safe2 += 1
        else:
            for idx in range(len(r)):
                relaxed = [ xv for xi, xv in enumerate(r) if xi != idx ]
                if check_if_safe(relaxed):
                    safe2 += 1
                    break

    print(f"part1 >> {safe}")
    print(f"part2 >> {safe2}")

main()