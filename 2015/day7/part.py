#!/usr/bin/env python3
import sys
import re

def calc_wire(root, outs):
    if type(root) is int:
        return root

    deps = outs[root]

    if type(deps) is int:
        return deps
    elif type(deps) is str:
        outs[root] = calc_wire(deps, outs)
    elif len(deps) == 2:
        outs[root] = ~calc_wire(deps[1], outs)
    elif deps[1] == "AND":
        outs[root] = calc_wire(deps[0], outs) & calc_wire(deps[2], outs)
    elif deps[1] == "OR":
        outs[root] = calc_wire(deps[0], outs) | calc_wire(deps[2], outs)
    elif deps[1] == "LSHIFT":
        outs[root] = calc_wire(deps[0], outs) << calc_wire(deps[2], outs)
    elif deps[1] == "RSHIFT":
        outs[root] = calc_wire(deps[0], outs) >> calc_wire(deps[2], outs)

    return outs[root]

def main():
    outs = {}

    re_num = re.compile(r"^\d+$")
    re_var = re.compile(r"^[a-z]+$")

    with open(sys.argv[1], "r") as file:
        for line in file:
            line = line.strip()

            lside, rside = line.split(" -> ")
            if re_num.match(lside):
                outs[rside] = int(lside)
            elif re_var.match(lside):
                outs[rside] = lside
            elif lside.startswith("NOT"):
                (op, b) = lside.split(" ")
                if re_num.match(b):
                    b = int(b)

                outs[rside] = (op, b)
            else:
                (a, op, b) = lside.split(" ")
                if re_num.match(a):
                    a = int(a)
                if re_num.match(b):
                    b = int(b)

                outs[rside] = (a, op, b)

    part_1 = outs.copy()
    a_wire = calc_wire("a", part_1)
    print("part1: ", a_wire)

    part_2 = outs.copy()
    part_2["b"] = a_wire
    a_wire = calc_wire("a", part_2)
    print("part2: ", a_wire)

main()
