#!/usr/bin/python3

import hashlib

def find_code(seed):
    salt = 0
    code = []
    while len(code) < 8:
        h = hashlib.md5()
        h.update(seed)
        h.update(str(salt).encode("utf-8"))

        hash = h.digest()[:4].hex()

        if hash.startswith("00000"):
            code.append(hash[5])
        salt += 1

    return "".join(code)

def find_code2(seed):
    salt = 0
    code = [ '' for _ in range(8) ]
    found = 0

    while found < 8:
        h = hashlib.md5()
        h.update(seed)
        h.update(str(salt).encode("utf-8"))

        hash = h.digest()[:4].hex()

        if hash.startswith("00000"):
            idx = ord(hash[5]) - ord('0')
            if idx >= 0 and idx < 8 and code[idx] == '':
                code[idx] = hash[6]
                found += 1

        salt += 1

    return "".join(code)

def main():
    test = find_code(b"abc")
    part1 = find_code(b"cxdnnyjw")
    part2 = find_code2(b"cxdnnyjw")

    print(f"test >> {test}")
    print(f"part1 >> {part1}")
    print(f"part2 >> {part2}")

main()

# binary - python3 3.12.5
#
#         User time (seconds): 32.94
#         System time (seconds): 0.00
#         Percent of CPU this job got: 99%
#
# binary - pypy3 7.3.17
#
#        User time (seconds): 111.73
#        System time (seconds): 0.04
#        Percent of CPU this job got: 99%
#
# Python3 won both pypy3 and go, that's crazy and exciting