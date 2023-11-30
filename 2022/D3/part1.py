
def main():
    score = 0

    with open("input.txt", "r") as file:
        for line in file:
            line = line.strip()
            start = line[ : len(line) // 2 ]
            end = line[ len(line) // 2 : ]

            overlap = set(start).intersection( set(end) )
            if len(overlap) == 1:
                sym = next(overlap.__iter__())

                lsym = ord(sym.lower()) - ord("a") + 1
                if sym.isupper():
                    lsym += 26

                print(sym, " -> ", lsym)
                score += lsym
            else:
                raise RuntimeError(":(")

    print(">>> ", score)

main()