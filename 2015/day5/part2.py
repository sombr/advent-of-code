#!/usr/bin/env python3
import sys

def main():
    with open(sys.argv[1], "r") as file:

        nice = 0
        for line in file:
            pairs = {}
            found_pair = False
            found_triplet = False

            prev_prev = "_"
            prev = "_"
            for idx, s in enumerate(line):
                pair = prev + s
                if pair in pairs:
                    if pairs[pair]["end"] < idx - 1:
                        pairs[pair]["count"] += 1
                else:
                    pairs[pair] = { "end": idx, "count": 1 }

                if pairs[pair]["count"] > 1:
                    found_pair = True
                if prev_prev == s:
                    found_triplet = True

                prev_prev = prev
                prev = s

            if found_pair and found_triplet:
                nice += 1

    print("nice strings part2: ", nice)

main()
