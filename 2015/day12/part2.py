#!/usr/bin/env python3

import json
import sys

def traverse(root):
    res = 0
    if type(root) is list:
        for e in root:
            res += traverse(e)
    elif type(root) is dict:
        candidate = 0
        for k, v in root.items():
            candidate += traverse(v)
            if v == "red":
                return res
        res += candidate
    elif type(root) is int:
        res += root
    elif type(root) is str:
        pass
    else:
        raise RuntimeError(f"unknown type: {type(root)}")
    return res

def main():
    with open(sys.argv[1], "r") as file:
        data = json.load(file)
    
    part2 = traverse(data)
    print(f">>> part2: {part2}")

main()