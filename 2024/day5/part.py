#!/usr/bin/python3

import sys
from functools import cmp_to_key

def validate_seq(rules, s):
    invalid = set()

    for idx in range(len(s)-1, -1, -1):
        page = s[idx]
        if page in invalid:
            return False
        for after_page in rules.get(page, set()):
            invalid.add(after_page)

    return True

def make_comparison_func(rules):
    def comparison(a, b):
        if a in rules and b in rules[a]:
            return -1
        if b in rules and a in rules[b]:
            return 1
        return 0
    return cmp_to_key(comparison)

def main():
    rules = {}
    seqs = []

    with open(sys.argv[1], "r") as file:
        for line in file:
            line = line.strip()
            if line.find("|") > 0:
                # rule line
                before, after = ( int(x) for x in line.split("|") )
                rules[before] = rules.get(before, set())
                rules[before].add(after)
            elif line.find(",") > 0:
                # seq line
                pages = [ int(x) for x in line.split(",") ]
                seqs.append(pages)

    cmp_f = make_comparison_func(rules)

    valid_mid_page_sum = 0
    invalid_mid_page_sum = 0
    for seq in seqs:
        is_valid = validate_seq(rules, seq)
        if is_valid:
            valid_mid_page_sum += seq[ len(seq) // 2 ]
        else:
            seq.sort(key=cmp_f)
            assert(validate_seq(rules, seq))

            invalid_mid_page_sum += seq[ len(seq) // 2 ]

    print(f"part1 >> {valid_mid_page_sum}")
    print(f"part2 >> {invalid_mid_page_sum}")

main()
