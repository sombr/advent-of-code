#!/usr/bin/python3

import sys

def find_len(content):
    res = 0
    idx = 0

    control = []
    while idx < len(content):
        if content[idx] == '(':
            control.append( content[idx] )
            idx += 1
        elif content[idx] == ')':
            # do something
            cseq = "".join(control[1:])
            control = []
            span, reps = [ int(x) for x in cseq.split("x") ]

            idx += 1

            subspan = find_len( content[idx:idx+span] )
            res += subspan*reps

            idx += span
        elif len(control) > 0:
            control.append( content[idx] )
            idx += 1
        else:
            res += 1
            idx += 1

    return res

def main():
    lines = None
    with open(sys.argv[1], "r") as file:
        lines = file.readlines()
    
    for content in lines:
        content = content.strip()
        slen = find_len(content)
        print(f">> part2 {slen}")

main()