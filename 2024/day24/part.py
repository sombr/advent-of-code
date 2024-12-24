#!/usr/bin/python3

import sys
from tqdm import tqdm

def load_input(filename):
    wires = {}
    links = {}

    readingWires = True
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line == "":
                readingWires = False
                continue

            if readingWires:
                w, v = line.split(": ")
                wires[w] = int(v)
            else:
                a, op, b, _, c = line.split()
                links[c] = (op, a, b)

    return wires, links

def compute_values(start, state, links):
    if start in state:
        return state[start]

    if start in links:
        op, a, b = links[start]
        value = None
        match op:
            case "AND":
                value = compute_values(a, state, links) * compute_values(b, state, links)
            case "OR":
                value = min(compute_values(a, state, links) + compute_values(b, state, links), 1)
            case "XOR":
                value = (compute_values(a, state, links) + compute_values(b, state, links)) % 2

        state[start] = value

    return value

def num2wires(num, prefix, size, acc_wires):
    for offset in range(size):
        name = "%s%02d" % (prefix, offset)
        acc_wires[name] = (num >> offset) & 1

def compute_output(wires, links):
    total = 0
    state = wires.copy()
    for wire in links.keys():
        if wire.startswith("z"):
            value = compute_values(wire, state, links)

            pos = int(wire[1:])
            total = total | (value << pos)

    return total

def main():
    wires, links = load_input(sys.argv[1])

    total = 0
    res = []
    state = wires.copy()
    for wire in links.keys():
        if wire.startswith("z"):
            value = compute_values(wire, state, links)
            res.append( ( wire, value ) )

            pos = int(wire[1:])
            total = total | (value << pos)

    print(res)
    print(total)

    shape_x = len([ x for x in wires.keys() if x.startswith("x") ])
    shape_y = len([ x for x in wires.keys() if x.startswith("y") ])
    shape_z = len([ x for x in links.keys() if x.startswith("z") ])

    print(shape_x, shape_y, shape_z)

    # fuzzing
    incorrect_outs = {}
    for x in tqdm(range(0, (1<<shape_x)-1, 131123182323)):
        for y in range(0, (1<<shape_y)-1, 121291271233):
            wires = {}
            num2wires(x, "x", shape_x, wires)
            num2wires(y, "y", shape_y, wires)

            value = compute_output(wires, links)

            true_answer = x+y

            for idx in range(shape_z):
                ta = ((true_answer >> idx)&1)
                va = ((value >> idx)&1)
                name = "z%02d" % idx
                if ta != va:
                    incorrect_outs[name] = incorrect_outs.get(name, 0) + 1
    print(incorrect_outs)

main()
