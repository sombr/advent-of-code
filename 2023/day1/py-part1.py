#!/usr/bin/env python3

import sys

def main(input_file):
    # streaming line-by-line processing
    with open(input_file, "r") as file:
        total = 0
        for line in file:
            line = line.strip()

            digits = []
            for character in line:
                if character.isdigit():
                    digits.append(character)

            current = int(digits[0] + digits[-1])
            total += current

            print(f"line: {line}, res: {current}")

    print("result sum: ", total)

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} <input file>")
else:
    main(sys.argv[1])