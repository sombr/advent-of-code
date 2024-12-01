#!/usr/bin/python3

import sys

def main():
    lines = None
    with open(sys.argv[1], "r") as file:
        lines = file.readlines()
    
    for content in lines:
        content = content.strip()
        res = []
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

                for r in range(reps):
                    res.append( content[idx:idx+span] )

                idx += span
            elif len(control) > 0:
                control.append( content[idx] )
                idx += 1
            else:
                res.append( content[idx] )
                idx += 1

        decoded = "".join(res)
        print(f">> part1 {len(decoded)}")

main()