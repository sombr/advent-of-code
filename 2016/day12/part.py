#!/usr/bin/python3

import sys

def run_simulation(registers, instructions):
    ip = 0
    instructions_len = len(instructions)
    while ip >= 0 and ip < instructions_len:
        cmd, *ps = instructions[ip]
        match cmd:
            case "cpy":
                f, t = ps
                registers[t] = registers.get(f, f)
                ip += 1
            case "inc":
                registers[ ps[0] ] += 1
                ip += 1
            case "dec":
                registers[ ps[0] ] -= 1
                ip += 1
            case "jnz":
                r, o = ps
                if registers.get(r, r) != 0:
                    ip += o
                else:
                    ip += 1

def main():
    instructions = []
    registers = {
            "a": 0,
            "b": 0,
            "c": 0,
            "d": 0
    }

    with open(sys.argv[1], "r") as file:
        for line in file:
            cmd, *params = line.strip().split()
            params = [ int(p) if p not in registers else p for p in params ]

            instructions.append( (cmd, *params) )

    run_simulation(registers, instructions)
    print(f">> part1 a = {registers['a']}")

    registers = {
            "a": 0,
            "b": 0,
            "c": 1,
            "d": 0
    }
    run_simulation(registers, instructions)
    print(f">> part2 a = {registers['a']}")


main()
