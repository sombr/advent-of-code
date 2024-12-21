#!/usr/bin/python3

import sys
from functools import cache

def load_data(filename):
    towel = None
    patterns = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if towel is None:
                towel = set(line.split(", "))
            elif len(line) > 0:
                patterns.append(line)
    return towel, patterns

@cache
def find_compositions(p, towels):
    if p == "":
        return 1

    count = 0
    for t in towels:
        if p.startswith(t):
            prefix = len(t)
            count += find_compositions(p[prefix:], towels)

    return count

def main():
    towels, patterns = load_data(sys.argv[1])

    possible = 0
    total = 0
    for p in patterns:
        count = find_compositions(p, tuple(towels))
        total += count
        if count > 0:
            possible += 1

    print(f"part1 >> {possible}")
    print(f"part2 >> {total}")

main()
