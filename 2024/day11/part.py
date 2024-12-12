#!/usr/bin/python3

import sys
from functools import cache

@cache
def blink_one(s):
    st = str(s)
    l = len(st)
    if s == 0:
        return [1]
    elif l % 2 == 0:
        return [
            int(st[:l//2]),
            int(st[l//2:])
        ]
    else:
        return [s*2024]

def main():
    stones_start = []
    with open(sys.argv[1], "r") as file:
        line = file.readline().strip()
        stones_start = [ int(x) for x in line.split() ]

    stones = {}
    for s in stones_start:
        stones[s] = stones.get(s, 0) + 1

    for bl in range(25): # blinks
        new_stones = {}
        for s, c in stones.items():
            for r in blink_one(s):
                new_stones[r] = new_stones.get(r, 0) + stones[s]

        stones = new_stones

        print(f">> blink {bl} len:{len(stones)}")

    print("part 1: >> ", sum(stones.values()))

    for bl in range(75 - 25): # blinks
        new_stones = {}
        for s, c in stones.items():
            for r in blink_one(s):
                new_stones[r] = new_stones.get(r, 0) + stones[s]

        stones = new_stones

        print(f">> blink {bl} len:{len(stones)}")

    print("part 2: >> ", sum(stones.values()))

main()
