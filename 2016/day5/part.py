#!/usr/bin/python3

import hashlib

def find_code(seed):
    salt = 0
    code = []
    while len(code) < 8:
        h = hashlib.md5()
        joint = (seed + str(salt)).encode("utf8")

        h.update(joint)
        hash = h.hexdigest()

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
        joint = (seed + str(salt)).encode("utf8")

        h.update(joint)
        hash = h.hexdigest()

        if hash.startswith("00000"):
            idx = ord(hash[5]) - ord('0')
            if idx >= 0 and idx < 8 and code[idx] == '':
                code[idx] = hash[6]
                found += 1

        salt += 1

    return "".join(code)

def main():
    test = find_code("abc")
    part1 = find_code("cxdnnyjw")
    part2 = find_code2("cxdnnyjw")

    print(f"test >> {test}")
    print(f"part1 >> {part1}")
    print(f"part2 >> {part2}")

main()