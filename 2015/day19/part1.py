#!/usr/bin/python3
import sys

def compute_replacement(subs, string):
    res = set()

    for s, ts in subs.items():
        parts = string.split(s)
        if len(parts) == 1:
            continue # not found

        endpos = len(parts)
        for pos in range(1, endpos):
            for t in ts:
                newstr = parts.copy()
                for ipos in range(endpos-1, 0, -1):
                    newstr.insert(ipos, t if pos == ipos else s)
                res.add( "".join(newstr) )

    return res


def main():
    subs = {}
    start = ""

    with open(sys.argv[1], "r") as file:
        for line in file:
            line = line.strip()
            parts = line.split(" => ")
            if len(parts) == 2:
                subs[parts[0]] = subs.get(parts[0], [])
                subs[parts[0]].append(parts[1])
            else:
                start = line

    print( subs, start )

    reps = compute_replacement(subs, start)
    print(reps)
    print(f"part1: {len(reps)}")

main()