#!/usr/bin/python3
import sys
import math

def backtrack(string, top, subs, steps, current_best):
    if string == "e":
        return steps

    if steps >= current_best[0]:
        return current_best[0]
    
    for t in top:
        if t in string:
            for s in subs[t]:
                newstr = string.replace(t, s, count=1)
                found_steps = backtrack(newstr, top, subs, steps+1, current_best)
                if found_steps < current_best[0]:
                    print(f"> found new best {found_steps} - current best {current_best}")
                    current_best[0] = found_steps

    return current_best[0]

def main():
    subs = {}
    target = ""

    with open(sys.argv[1], "r") as file:
        for line in file:
            line = line.strip()
            parts = line.split(" => ")
            if len(parts) == 2:
                subs[parts[1]] = subs.get(parts[1], [])
                subs[parts[1]].append(parts[0])
            else:
                target = line

    for sx in subs.values():
        sx.sort()

    candidates = sorted( subs.keys(), key=lambda x: (-len(x), len(subs[x][0])))

    curbest = [math.inf]
    steps = backtrack(target, candidates, subs, 0, curbest)

    print(f"part2 >>> {steps}")

main()