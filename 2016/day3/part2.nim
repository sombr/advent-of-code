import std/re
import strutils

proc main() =
    let content = readFile("input.txt").strip()
    let lines = content.split("\n")

    var cols: array[3, seq[int]] = [ @[], @[], @[] ]
    var triangles = 0

    for line in lines:
        let parts = split(line.strip(), re"\s+")
        if len(parts) < 3:
            continue

        for pidx in 0..len(parts)-1:
            let vertex = parseInt(parts[pidx])
            cols[pidx].add(vertex)

    for col in cols:
        for t in countup(0, len(col)-1, 3):
            if col[t] + col[t+1] > col[t+2] and col[t+1] + col[t+2] > col[t] and col[t] + col[t+2] > col[t+1]:
                triangles += 1

    echo ">>> part2: ", triangles

main()
