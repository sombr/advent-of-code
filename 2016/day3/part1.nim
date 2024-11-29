import std/re
import strutils

proc main() =
    let content = readFile("input.txt").strip()
    let lines = content.split("\n")

    var triangles: seq[array[3, int]] = @[]
    for line in lines:
        let parts = split(line.strip(), re"\s+")
        if len(parts) < 3:
            continue

        var vxs: array[3, int] = [0, 0, 0]
        for pidx in 0..len(parts)-1:
            vxs[pidx] = parseInt(parts[pidx])

        if vxs[0] + vxs[1] > vxs[2] and vxs[1] + vxs[2] > vxs[0] and vxs[0] + vxs[2] > vxs[1]:
            triangles.add( vxs )

    echo ">>> part1: ", len(triangles)

main()
