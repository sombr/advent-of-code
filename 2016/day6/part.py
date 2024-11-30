#!/usr/bin/python3

import sys

def gen_pos_counts():
    return [ 0 for _ in range(26) ]

def main():
    counts = []

    with open(sys.argv[1], "r") as file:
        for line in file:
            line = line.strip()
            if len(counts) == 0:
                counts = [ gen_pos_counts() for _ in range(len(line)) ]

            for idx, c in enumerate(line.strip()):
                counts[idx][ord(c) - ord('a')] += 1

    message = []
    message2 = []
    for ls in counts:
        maxidx = -1
        maxval = -1
        minidx = -1
        minval = 1_000_000
        for idx, c in enumerate(ls):
            if c > maxval:
                maxval = c
                maxidx = idx
            if c < minval:
                minval = c
                minidx = idx
        message.append(chr( ord('a') + maxidx ))
        message2.append(chr( ord('a') + minidx ))

    print("part1 >>>", "".join(message))
    print("part2 >>>", "".join(message2))

main()