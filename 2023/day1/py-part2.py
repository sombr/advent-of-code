#!/usr/bin/env python3

import sys

WORDS: list[str] = ["0", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
REV_WORDS: list[str] = [ "".join(reversed(w)) for w in WORDS ]

def get_first_digit(line: str, word_map) -> str:
    num_pos = -1
    digit = ""
    for idx, sym in enumerate(line):
        if sym.isdigit():
            num_pos = idx
            digit = sym
            break

    line = line[:num_pos]
    for idx, word in enumerate(word_map):
        pos = line.find(word)
        if pos < 0:
            continue
        if num_pos < 0 or num_pos > pos:
            num_pos = pos
            digit = str(idx)

    return digit

def main(input_file):
    # streaming line-by-line processing
    with open(input_file, "r") as file:
        total = 0
        for line in file:
            line = line.strip()
            invline = "".join(reversed(line))

            number = get_first_digit(line, WORDS) + get_first_digit(invline, REV_WORDS)

            current = int(number)
            total += current

    print("result sum: ", total)

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} <input file>")
else:
    main(sys.argv[1])