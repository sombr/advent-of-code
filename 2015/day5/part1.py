#!/usr/bin/env python3

def main():
    with open("input.txt", "r") as file:
        vset = set(["a", "e", "i", "o", "u"])
        bset = set(["ab", "cd", "pq", "xy"])

        nice = 0
        for line in file:
            vowels = 0
            doubles = 0
            banned = 0

            dpart = False
            prev = ""
            for s in line:
                if s in vset:
                    vowels += 1
                if s == prev and (not dpart):
                    doubles += 1
                    dpart = True
                if (prev+s) in bset:
                    banned += 1
                dpart = False
                prev = s
            
            is_nice = vowels >= 3 and doubles > 0 and banned <= 0
            if is_nice:
                nice += 1
    print("nice strings part1: ", nice)

main()
