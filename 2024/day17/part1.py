#!/usr/bin/python3

import sys

def process_combo(state, val):
    if val >= 0 and val < 4:
        return val
    if val >= 7:
        raise RuntimeError(":( 7")
    return state[ val - 4 ]

def adv(state, operand, ip, out):
    numerator = state[0] # A
    denominator = 2**process_combo(state, operand)

    res = numerator // denominator
    state[0] = res

    return True

def bxl(state, operand, ip, out):
    res = state[1] ^ operand # B
    state[1] = res

    return True

def bst(state, operand, ip, out):
    res = process_combo(state, operand) % 8
    state[1] = res # B

    return True

def jnz(state, operand, ip, out):
    if state[0] == 0:
        return True

    ip[0] = operand
    return False

def bxc(state, operand, ip, out):
    res = state[1] ^ state[2]
    state[1] = res

    return True

def out(state, operand, ip, out_list):
    res = process_combo(state, operand) % 8
    out_list.append(res)

    return True

def bdv(state, operand, ip, out):
    numerator = state[0] # A
    denominator = 2**process_combo(state, operand)

    res = numerator // denominator
    state[1] = res

    return True

def cdv(state, operand, ip, out):
    numerator = state[0] # A
    denominator = 2**process_combo(state, operand)

    res = numerator // denominator
    state[2] = res

    return True

def load_input(filename):
    registers = []
    instructions = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("Register"):
                registers.append( int(line.split()[-1]) )
            if line.startswith("Program"):
                instructions = [ int(v) for v in line.split()[-1].split(",") ]

    return registers, tuple(instructions)


def run_program(initial_state, program):
    state = [ x for x in initial_state ]

    ip = [0]

    opmap = [ adv, bxl, bst, jnz, bxc, out, bdv, cdv ]

    out_list = []
    while ip[0] >= 0 and ip[0] < len(program):
        opcode = program[ ip[0] ]
        operand = program[ ip[0] + 1 ]

        if opmap[opcode](state, operand, ip, out_list):
            ip[0] += 2

    return tuple(out_list)

def main():
    state, program = load_input(sys.argv[1])

    out = run_program(state, program)
    print("part1 >>> ", ",".join( ( str(v) for v in out )))

main()
