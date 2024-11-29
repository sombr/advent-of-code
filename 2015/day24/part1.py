#!/usr/bin/python3

import math

WEIGHTS = [1,3,5,11,13,17,19,23,29,31,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113]


def check_in_bitmap(bitmap: int, idx: int):
    return ((1 << idx) & bitmap) != 0


def add_to_bitmap(bitmap: int, idx: int):
    return ((1 << idx) | bitmap)


def bitmap_to_items(bitmap: int, ws: list):
    res = []
    for idx, w in enumerate(ws):
        if check_in_bitmap(bitmap, idx):
            res.append(w)
    return res


def get_groups_of_weight(
        ws: tuple[int],
        selected: int,
        target: int,
        current: int,
        acc: set[int],
        mem: set[int]):

    if current == target:
        acc.add(selected)
        return
    elif current > target:
        return
    elif selected in mem:
        return  # we've seen this already

    for idx, w in enumerate(ws):
        if not check_in_bitmap(selected, idx):
            selnew = add_to_bitmap(selected, idx)
            current += w

            get_groups_of_weight(ws, selnew, target, current, acc, mem)

            current -= w

    mem.add(selected)

    return


def main():
    total_weight = sum(WEIGHTS)
    target_weight = total_weight // 3

    revws = tuple(sorted(WEIGHTS, reverse=True))

    print(f"total weight: {total_weight}, target: {target_weight}, num of items: {len(WEIGHTS)}")

    groups = set()
    get_groups_of_weight(revws, 0, target_weight, 0, groups, set())

    groups = sorted([ bitmap_to_items(bm, revws) for bm in groups ], key=lambda x: len(x))

    minlen = len(WEIGHTS) + 100
    for g in groups:
        gsum = sum(g)
        minlen = min(minlen, len(g))
        print(f"group len: {len(g)} sum: {gsum} items: {g}")

    print(">>> First (min size) group candidates:")
    first = sorted([ (math.prod(g), g) for g in groups if len(g) == minlen ])

    for fc in first:
        print(f"> QE: {fc[0]} group: {fc[1]}")

    print(f"part 1 >>> {first[0]}")

main()
