
def main():
    maxcal = 0

    with open("input.txt", "r") as file:
        curcal = 0
        for line in file:
            line = line.strip()
            if line == "":
                maxcal = max(maxcal, curcal)
                curcal = 0
            else:
                curcal += int(line)

    print(">>> ", maxcal)


main()