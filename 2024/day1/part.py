#!/usr/bin/python3

import sys

def main():
    list1 = []
    list2 = []

    list2counts = {}
    with open(sys.argv[1], "r") as file:
        for line in file:
            ps = [ int(x) for x in line.strip().split() ]
            list1.append(ps[0])
            list2.append(ps[1])

            list2counts[ps[1]] = list2counts.get(ps[1], 0) + 1

    list1.sort()
    list2.sort()

    delta_sum = 0
    for v1, v2 in zip(list1, list2):
        delta_sum += abs(v1 - v2)

    print(f"part 1 >>> {delta_sum}")

    # similarity
    similarity = 0
    for vl in list1:
        similarity += vl * list2counts.get(vl,  0)

    print(f"part 2 >>> {similarity}")

main()