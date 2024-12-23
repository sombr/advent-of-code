#!/usr/bin/python3

import sys
from collections import deque

def get_secret(seed):
    prune_mask = (1 << 24) - 1 # this is 16777216 - 1

    seed = ( seed ^ ( seed << 6 ) ) & prune_mask
    seed = ( seed ^ ( seed >> 5 ) ) & prune_mask
    seed = ( seed ^ ( seed << 11 ) ) & prune_mask

    return seed

def get_ith_secret(seed, count):
    for _ in range(count):
        seed = get_secret(seed)
    return seed

def get_price(seed):
    return seed % 10

def main():
    seeds = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            seeds.append(int(line))

    total = 0
    for seed in seeds:
        hop = get_ith_secret(seed, 2000)
        price = get_price(hop)
        print(f"{seed}: {hop} price {price}")

        total += hop

    print("part1 >> ", total)

    seqs = {}
    for seed in seeds:
        prices = [ get_price(seed) ]
        for _ in range(2000):
            seed = get_secret(seed)
            prices.append( get_price( seed ) )

        deltas = []
        for idx in range(1, len(prices)):
            deltas.append(prices[idx] - prices[idx-1])

        seen = set()
        window = deque()
        for idx, dp in enumerate(deltas):
            window.append(dp)
            if len(window) == 4:
                seq = tuple(window)
                if seq in seen:
                    pass
                else:
                    seen.add(seq)
                    seqs[seq] = seqs.get(seq, 0) + prices[idx+1]
                window.popleft()

    sales = max(seqs.items(), key=lambda x: x[1])
    print(sales)

main()
