#!/usr/bin/python3

import sys
import math

def count(target, coins, used_containers):
    if target == 0:
        return 1, used_containers, 1
    if target < 0:
        return 0, math.inf, 1
    if len(coins) == 0:
        return 0, math.inf, 1
    p1, min_use1, min_use_count1 = count(target, coins[1:], used_containers)
    p2, min_use2, min_use_count2 = count(target - coins[0], coins[1:], used_containers+1)
    
    min_use = min(min_use1, min_use2)
    min_use_count = 0
    if min_use1 == min_use:
        min_use_count += min_use_count1
    if min_use2 == min_use:
        min_use_count += min_use_count2

    return p1+p2, min_use, min_use_count
    

def main():
    buckets = []
    with open(sys.argv[1], "r") as file:
        buckets = sorted([ int(x) for x in file.readlines() ])

    res, min_use, min_use_count = count(150, buckets, 0)
    print(f"part1: {res}")
    print(f"part2: {min_use_count} for the min of {min_use} containers")

main()