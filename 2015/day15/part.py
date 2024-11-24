#!/usr/bin/env python3
import sys
import numpy as np

total = 100

def make_cases(count, acc):
    if count == 0:
        return acc
    res = []
    for v in acc:
        for x in range(101):
            row = v + [x]
            if sum(row) <= 100:
                res.append(row)
    return make_cases(count-1, res)

def main():
    coefs = []
    # Sugar: capacity 0, durability 0, flavor -2, texture 2, calories 1
    with open(sys.argv[1], "r") as file:
        for line in file:
            (name, parts) = line.split(": ")
            coefs.append([ int(p.split(" ")[-1]) for p in parts.split(", ") ])

    coefs = np.array(coefs, dtype=np.int32)
    cases = np.array([ r for r in make_cases(coefs.shape[0], [[]]) if sum(r) == 100 ])

    coefs_no_cal = coefs[:, :-1]

    vol = cases.dot(coefs_no_cal)
    vol = np.prod( np.clip(vol, 0, 5_000_000), axis=1 )
    print(vol.shape)
    print("part1 max >> ", np.max(vol))

    vol = cases.dot(coefs)
    at500cal = (vol[:, -1] == 500).astype("int").reshape(-1, 1)
    vol = (vol * at500cal)[:, :-1]

    vol = np.prod( np.clip(vol, 0, 5_000_000), axis=1 )
    print(vol.shape)
    print("part2 max >> ", np.max(vol))

main()