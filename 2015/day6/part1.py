#!/usr/bin/env python3
import numpy as np
import sys

def main():
    scr = np.zeros( (1000, 1000), dtype=np.byte )

    with open("input.txt", "r") as file:
        for line in file:
            line = line.replace("turn ", "")

            (action, s, _, e) = line.split(" ")

            (sx, sy) = ( int(x) for x in s.split(",") )
            (ex, ey) = ( int(x) for x in e.split(",") )

            match action:
                case "on":
                    scr[sx:ex+1, sy:ey+1] = 1
                case "off":
                    scr[sx:ex+1, sy:ey+1] = 0
                case "toggle":
                    scr[sx:ex+1, sy:ey+1] = 1 - scr[sx:ex+1, sy:ey+1]

            print(action, (sx, sy), (ex, ey))
    lights_on = np.sum(scr > 0)
    print(f"part 1: {lights_on}")

main()
