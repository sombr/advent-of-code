
# rules A - Rock, B - Paper, C - Scissors
# Opponent -- [ Loss, Tie, Win ]
rules = {
    "A": ("C", "A", "B"),
    "B": ("A", "B", "C"),
    "C": ("B", "C", "A")
}

cost = {
    "A": 1,
    "B": 2,
    "C": 3
}

rmap = {
    "X": 0,
    "Y": 1,
    "Z": 2
}

def main():
    score = 0
    with open("input.txt", "r") as file:
        for line in file:
            (o, r) = line.strip().split(" ")
            ri = rmap[r]
            choice = rules[o][ri]

            score += 3 * ri + cost[choice]

    print(">>> ", score)

main()