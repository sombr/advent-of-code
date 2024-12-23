#!/usr/bin/python3

import sys
import math
from collections import deque

NUM_PAD = [
    "789",
    "456",
    "123",
    "X0A"
]

KEY_PAD = [
    "X^A",
    "<v>"
]

DELTA_MOVE = {
    ">": (0,1),
    "^": (-1,0),
    "v": (1,0),
    "<": (0,-1),
}

def bfsall(pad, start, DM):
    r_, c_ = start

    paths = {}

    visited = {}
    q = deque([ (r_,c_,[]) ])
    while q:
        r, c, path = q.popleft()

        seq = tuple(path + ["A"])

        if len(seq) > visited.get( (r,c), math.inf ):
            continue

        visited[ (r,c) ] = min(visited.get( (r,c), math.inf ), len(seq))
        paths[ pad[r][c] ] = paths.get( pad[r][c], set() )
        paths[ pad[r][c] ].add(seq)

        for move, (dr, dc) in DM.items():
            nr, nc = r+dr, c+dc

            if nr < 0 or nc < 0 or nr >= len(pad) or nc >= len(pad[0]):
                continue
            if pad[nr][nc] == "X":
                continue

            q.append( (nr,nc,path + [move]) )

    return paths

def bfs(pad, start, DM):
    r_, c_ = start

    paths = {}

    visited = set()
    q = deque([ (r_,c_,[]) ])
    while q:
        r, c, path = q.popleft()

        seq = tuple(path + ["A"])

        if (r,c) in visited:
            continue

        visited.add( (r,c) )

        paths[ pad[r][c] ] = seq

        for move, (dr, dc) in DM.items():
            nr, nc = r+dr, c+dc

            if nr < 0 or nc < 0 or nr >= len(pad) or nc >= len(pad[0]):
                continue
            if pad[nr][nc] == "X":
                continue

            q.append( (nr,nc,path + [move]) )

    return paths

def precompute_moves(pad, DM, compute_all = False):
    reach = {}

    for ridx, row in enumerate(pad):
        for cidx, val in enumerate(row):
            if val == "X":
                continue
            if compute_all:
                reach[val] = bfsall(pad, (ridx, cidx), DM)
            else:
                reach[val] = bfs(pad, (ridx, cidx), DM)

    return reach

def encode_moves_lazy(precompute, code):
    prev = "A"
    for b in code:
        for m in precompute[prev][b]:
            yield m
        prev = b

def encode_moves(precompute, code):
    return "".join(encode_moves_lazy(precompute, code))

def precompute_pads():
    kr_initial = precompute_moves(KEY_PAD, DELTA_MOVE, False)

    key_reach = precompute_moves(KEY_PAD, DELTA_MOVE, True)
    for f in key_reach.keys():
        for t in key_reach[f].keys():
            paths = key_reach[f][t]
            path = min(paths, key = lambda path: len(encode_moves(kr_initial, encode_moves(kr_initial, path))))
            key_reach[f][t] = path

    num_reach = precompute_moves(NUM_PAD, DELTA_MOVE, True)
    for f in num_reach.keys():
        for t in num_reach[f].keys():
            paths = num_reach[f][t]
            path = min(paths, key = lambda path: len(encode_moves(key_reach, encode_moves(key_reach, path))))
            num_reach[f][t] = path


    return num_reach, key_reach

def main():
    lines = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            lines.append( line.strip() )

    num_reach, key_reach = precompute_pads()

    print("NUM")
    for f, ts in sorted(num_reach.items()):
        for t, val in sorted(ts.items()):
            v = "".join(val)
            print(f"{f} {t} :: {v}")
    print("KEY")
    for f, ts in sorted(key_reach.items()):
        for t, val in sorted(ts.items()):
            v = "".join(val)
            print(f"{f} {t} :: {v}")

    total = 0
    for code in lines:
        num = int(code[:-1])
        moves = encode_moves_lazy(key_reach, encode_moves_lazy(key_reach, encode_moves_lazy(num_reach, code)))
        moves = "".join(moves)

        complexity = num * len(moves)
        total += complexity

        print(f"{code}: ({len(moves)}*{num}) {moves}")

    print(f">>> part1 {total}")

    exit(1)

    # part 2
    total = 0
    for code in lines:
        num = int(code[:-1])

        moves = encode_moves_lazy(num_reach, code)
        for idx in range(25):
            print(f"{code} encoded {idx+1} times")
            moves = encode_moves_lazy(key_reach, moves)

        mlen = 0
        for _ in moves:
            if mlen % 100_000_000 == 0:
                print(f"{code} passing {mlen}")
            mlen += 1

        complexity = num * mlen
        total += complexity

        print(f"{code}: ({mlen}*{num})")

    print(f">>> part2 {total}")

main()
