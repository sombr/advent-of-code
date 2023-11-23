import heapq

def main():
    # complexity: N*logM where N - number of input lines, M - top size (3)
    top = []

    with open("input.txt", "r") as file:
        cur = 0
        for line in file:
            line = line.strip()
            if line == "":
                heapq.heappush(top, cur)
                cur = 0
                if len(top) > 3:
                    heapq.heappop(top)
            else:
                cur += int(line)

    print(">>>", sum(top))

main()