
# combinations lookup
loss = {
    ("A", "C"),
    ("B", "A"),
    ("C", "B")
}

xyz_map = {
    "X": "A",
    "Y": "B",
    "Z": "C"
}

value = {
    "X": 1,
    "Y": 2,
    "Z": 3
}

def main():
    score = 0
    with open("input.txt", "r") as file:
        for line in file:
            round_score = 0

            (o, m) = line.strip().split(" ")
            n = xyz_map[m]
            v = value[m]

            round_score += v

            if (o, n) in loss:
                pass # 0
            elif o == n:
                round_score += 3
            else:
                round_score += 6 # win

            print(f"round: {o} {m} score: {round_score} (val: {v}) (loss: { (o,n) in loss })")

            score += round_score

    print(">> ", score)

main()