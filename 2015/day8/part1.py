#!/usr/bin/env python3
import sys

def main():
    symbols = 0
    memory = 0

    with open(sys.argv[1], "r") as file:
        for line in file:
            line = line.strip()

            sym_rep = len(line)
            mem_rep = 0

            skip_count = 0
            for (s, n) in zip(line, line[1:]):
                if skip_count > 0:
                    skip_count -= 1
                    continue

                if s == '"':
                    continue

                if s != "\\":
                    mem_rep += 1
                    continue

                if n == "\\" or n == '"':
                    mem_rep += 1
                    skip_count = 1
                    continue

                if n == "x":
                    mem_rep += 1
                    skip_count = 3
                    continue

            symbols += sym_rep
            memory += mem_rep

    print(f"part 1 - symbols:{symbols} memory:{memory} answer:{symbols - memory}")

main()
