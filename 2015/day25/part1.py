#!/usr/bin/pypy3

import math

CODES = [
    [20151125, 18749137, 17289845, 30943339, 10071777, 33511524],
    [31916031, 21629792, 16929656, 7726640, 15514188, 4041754],
    [16080970, 8057251, 1601130, 7981243, 11661866, 16474243],
    [24592653, 32451966, 21345942, 9380097, 10600672, 31527494],
    [77061, 17552253, 28094349, 6899651, 9250759, 31663883],
    [33071741, 6796745, 25397450, 24659492, 1534922, 27995004]
]

def vec2_to_seq(r, c):
    diag = r + c - 1
    # 1 | 2 | 3 | 4 ...
    # (end + 1)*end / 2
    
    prev_d = diag - 1

    elements_before = ((prev_d + 1)*prev_d) // 2
    seq_idx = elements_before + c

    return seq_idx

def find_code():
    prev = None
    # move in diagonals:
    for d in range(1, 5_000_000):
        for c in range(1, d+1):
            if d == 1 and c == 1:
                prev = CODES[0][0]
                continue

            r = d - c + 1
            idx = vec2_to_seq(r,c)
            #print(f">> diag:{d} ({r},{c}) --> {idx}")

            code = (prev * 252533) % 33554393
            prev = code

            # result
            if r == 2981 and c == 3075:
                return code

def main():
    code = find_code()
    print(f"part1 >> {code}")

main()
