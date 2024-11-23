#!/usr/bin/env python3

import json
import sys

def traverse(root):
    res = 0
    if type(root) is list:
        for e in root:
            res += traverse(e)
    elif type(root) is dict:
        for k, v in root.items():
            res += traverse(v)
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
    
    part1 = traverse(data)
    print(f">>> part1: {part1}")

main()