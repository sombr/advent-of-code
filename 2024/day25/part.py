#!/usr/bin/python3

import sys

def load_input(filename):
    content = None
    with open(filename, "r") as file:
        content = file.read().strip()

    blocks = content.split("\n\n")

    keys = []
    locks = []

    for block in blocks:
        rows = block.strip().split("\n")

        code = []
        top_filled = True

        for col in range(len(rows[0])):
            top_filled = top_filled and rows[0][col] == "#"
            filled = -1
            for row in rows:
                if row[col] == "#":
                    filled += 1
            code.append(filled)

        if top_filled:
            locks.append(tuple(code))
        else:
            keys.append(tuple(code))

    return keys, locks

def encode_height_to_bin(h, is_lock):
    h = h + 1
    if is_lock:
        # 0 0 0 0 0 0 0 1
        r = (1 << h) - 1
        return r
    else:
        f = (1 << 7) - 1
        r = (1 << (7-h)) - 1
        r = f - r
        return r

def encode_to_bin(code, is_lock):
    num = 0
    for c in code:
        num = num << 8
        num = num | encode_height_to_bin(c, is_lock)

    return num

def main():
    keys, locks = load_input(sys.argv[1])

    print(keys)
    print("--")
    print(locks)

    print("key 3 = ", bin(encode_height_to_bin(3, False)))
    print("lck 3 = ", bin(encode_height_to_bin(3, True)))
    print(keys[0], bin(encode_to_bin( keys[0], False )) )

    kbs = [ encode_to_bin(k, False) for k in keys ]
    lbs = [ encode_to_bin(l, True) for l in locks ]

    match = 0
    # find pairs
    for li, lock in enumerate(lbs):
        for ki, key in enumerate(kbs):
            if (key ^ lock) == (key | lock):
                match += 1
                print("found fit: ", locks[li], " key > ", keys[ki])
                print("lock: %50s" % bin(lock))
                print("key : %50s" % bin(key))

    print("part1 matches: ", match)

main()
