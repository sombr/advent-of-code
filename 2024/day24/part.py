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

def print_path(links, state, start, level):
    indent = level * 2
    if start in links:
        print(" " * indent, end = "")
        op, a, b = links[start]
        desc = str(level)

        if op == "XOR":
            if a.startswith("x") or a.startswith("y"):
                desc = f"SUM"
            else:
                desc = f"SUM+CARRY"
        elif op == "OR":
            desc = f"CARRY"
        elif op == "AND":
            if a.startswith("x") or b.startswith("y"):
                desc = f"BITCARRY"
            else:
                desc = f"CARRY"

        val = state[start]
        print(f"{start} ({desc}) [{val}] <= {a} {op} {b}")
        print_path(links, state, a, level+1)
        print_path(links, state, b, level+1)

def compute_values(start, state, links, level=0):
    if level > 100:
        return -1000

    if start in state:
        return state[start]

    value = -1000
    if start in links:
        op, a, b = links[start]
        match op:
            case "AND":
                value = compute_values(a, state, links, level+1) * compute_values(b, state, links, level+1)
            case "OR":
                value = min(compute_values(a, state, links, level+1) + compute_values(b, state, links, level+1), 1)
            case "XOR":
                value = (compute_values(a, state, links, level+1) + compute_values(b, state, links, level+1)) % 2

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

    return total, state

def check_correct(x, y, shape, links):
    wires = {}
    num2wires(x, "x", shape, wires)
    num2wires(y, "y", shape, wires)

    value, state = compute_output(wires, links)

    true_answer = x+y

    return value == true_answer

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

    wrong_offs = []
    for off in range(44):
        x = 1<<off
        y = 1<<off
        if not check_correct(x, y, shape_x, links):
            wrong_offs.append(off)

    print(wrong_offs)

    wrong_offs = []
    for off in range(44):
        x = 1<<off
        y = 1<<off+1
        if not check_correct(x, y, shape_x, links):
            wrong_offs.append(off)

    print(wrong_offs)

    wrong_offs = []
    for x in range(1<<43):
        y = 1
        if not check_correct(x, y, shape_x, links):
            wrong_offs.append(off)
            break

    print(wrong_offs)
    
    exit(1)

    gates = sorted(links.keys())
    for agi in range(len(gates)):
        ag = gates[agi]
        for bgi in range(agi+1, len(gates)):
            bg = gates[bgi]
            links[ag], links[bg] = links[bg], links[ag]

            all_correct = True
            for off in range(44):
                x = 1<<off
                y = 1<<off
                if not check_correct(x, y, shape_x, links):
                    all_correct = False
                y = 1<<off+1
                if not check_correct(x, y, shape_x, links):
                    all_correct = False
            if all_correct:
                print(f"found candidate for swap: {ag} <=> {bg}")

            links[ag], links[bg] = links[bg], links[ag]

    print(wrong_offs)

main()
