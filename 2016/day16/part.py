#!/usr/bin/python3

import os

def neg(xs):
    return "".join( ( "1" if x == "0" else "0" for x in reversed(xs) ) )

def extend(xs):
    return xs + "0" + neg(xs)

def checksum(xs):
    res = []
    idx = 0
    while idx < len(xs) - 1:
        if xs[idx] == xs[idx+1]:
            res.append("1")
        else:
            res.append("0")
        idx += 2
    return "".join(res)

def solve(seed, size):
    while len(seed) < size:
        seed = extend(seed)
    seed = seed[:size]

    chk = seed
    while True:
        chk = checksum(chk)
        if len(chk) % 2 != 0:
            return chk

    raise RuntimeError(":(")

def main():
    res = solve("01111001100111011", 272)
    print("part1: ", res)

    res = solve("01111001100111011", 35651584)
    print("part2: ", res)
main()
