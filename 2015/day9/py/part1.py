#!/usr/bin/env python3
# this is a travelling salesman problem which is NP hard
# the number of cities in the part 1 is relatively low though
# and we can just brute-force it.

import numpy as np
import sys
import time
from itertools import permutations

def backtrack(cost, num_cities, prev_city, current_cost, best_cost, visited, reducer):
    if current_cost > best_cost:
        return current_cost
    if visited == num_cities:
        return current_cost
    
    # where we can travel:
    for n in range(num_cities):
        if cost[n, n] < 0:
            continue # we've visited this already

        cost[n, n] = -1

        step_cost = 0 if prev_city < 0 else cost[prev_city, n]
        path_cost = backtrack(cost, num_cities, n, current_cost + step_cost, best_cost, visited+1, reducer)
        best_cost = reducer(path_cost, best_cost)

        cost[n, n] = 0

    return best_cost

def brute_force(cost, num_cities, best_cost, reducer):
    all_perms = permutations([ x for x in range(num_cities) ])

    for perm in all_perms:
        cur_cost = 0
        for idx in range(1, len(perm)):
            cur_cost += cost[perm[idx-1], perm[idx]]
        best_cost = reducer(cur_cost, best_cost)
    return best_cost

def main():
    place2idx = {}
    place2place2dist = {}

    with open(sys.argv[1], "r") as file:
        for line in file:
            line = line.strip()
            (start, _, end, _, dist) = line.split(" ")

            place2idx[start] = place2idx.get(start, len(place2idx))
            place2idx[end] = place2idx.get(end, len(place2idx))

            place2place2dist[start] = place2place2dist.get(start, {})
            place2place2dist[start][end] = dist

    mdist = np.zeros( (len(place2idx), len(place2idx)), dtype=np.int32 )
    for start, ends in place2place2dist.items():
        for end, dist in ends.items():
            mdist[ place2idx[start], place2idx[end] ] = dist
            mdist[ place2idx[end], place2idx[start] ] = dist

    print(place2idx)
    print(mdist)

    best_cost = backtrack(mdist, mdist.shape[0], -1, 0, np.inf, 0, min)
    print(f"best cost: {best_cost}")

    brute_cost = brute_force(mdist, mdist.shape[0], np.inf, min)
    print(f"brute cost: {brute_cost}")

    print("part 2, longest")

    best_cost = backtrack(mdist, mdist.shape[0], -1, 0, 0, 0, max)
    print(f"best cost: {best_cost}")

    brute_cost = brute_force(mdist, mdist.shape[0], 0, max)
    print(f"brute cost: {brute_cost}")

main()