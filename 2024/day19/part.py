#!/usr/bin/python3

import sys

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

def count_assemble(pattern, towels, mem):
    if pattern in mem:
        return mem[pattern]

    if len(pattern) < 1:
        return 0

    if len(pattern) == 1:
        if pattern in towels:
            return 1
        else:
            return 0

    count = 0
    if pattern in towels:
        count = 1

    for idx in range(1, len(pattern)):
        p1, p2 = pattern[:idx], pattern[idx:]

        c1 = count_assemble(p1, towels, mem)
        c2 = count_assemble(p2, towels, mem)

        count += c1*c2

    mem[pattern] = count
    return mem[pattern]

def main():
    towels, patterns = load_data(sys.argv[1])
    mem = {}

    count = 0
    for p in patterns:
        c = count_assemble(p, towels, mem)
        if c > 0:
            count += 1

    print(f"part1 >> {count}")

main()
