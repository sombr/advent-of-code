#!/usr/bin/env python3
import sys

def main():

    memory = 0
    string = 0

    with open(sys.argv[1], "r") as file:
        for line in file:
            line = line.strip()

            mem_len = len(line)
            str_len = 2

            for s in line:
                match s:
                    case '"':
                        str_len += 2
                    case "\\":
                        str_len += 2
                    case _:
                        str_len += 1

            memory += mem_len
            string += str_len

    print(f"part2: {string - memory}")

main()
