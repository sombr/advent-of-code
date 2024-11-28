#!/usr/bin/python3

import sys


def main():
    commands = []

    with open(sys.argv[1], "r") as file:
        for line in file:
            line = line.strip()

            cmd, args = line.split(" ", maxsplit=1)
            if args.find(",") > 0:
                args = args.split(", ")
            else:
                args = [args]

            commands.append( (cmd, args) )

    cidx = 0
    a = 1
    b = 0

    while cidx >= 0 and cidx < len(commands):
        cmd, args = commands[cidx]

        match cmd:
            case "hlf":
                if args[0] == "a":
                    a /= 2
                else:
                    b /= 2
                cidx += 1
            case "tpl":
                if args[0] == "a":
                    a *= 3
                else:
                    b *= 3
                cidx += 1
            case "inc":
                if args[0] == "a":
                    a += 1
                else:
                    b += 1
                cidx += 1
            case "jmp":
                offset = int(args[0])
                cidx += offset
            case "jie":
                reg, offset = args
                rval = a if reg == "a" else b
                offset = int(offset)
                if rval % 2 == 0:
                    cidx += offset
                else:
                    cidx += 1
            case "jio":
                reg, offset = args
                rval = a if reg == "a" else b
                offset = int(offset)
                if rval == 1:
                    cidx += offset
                else:
                    cidx += 1
            case _:
                raise RuntimeError(f"unknown command: {cmd}")

    print(f">> part1, b = {b}")

main()
