# part1

import sets
import options
import strutils

proc main =
    let file = readFile("input.txt").strip()
    let parts = file.split(", ")

    var visited_positions: HashSet[tuple[r:int, c:int]]

    var row = 0
    var col = 0

    const dir_deltas = [ (-1, 0), (0, 1), (1, 0), (0, -1) ]
    var dir = 0

    var first_twice: Option[tuple[r:int, c:int]]

    for p in parts:
        let turn = p[0]
        let dist = parseInt(p[1..len(p)-1])

        if turn == 'R':
            dir = (dir + 1) mod len(dir_deltas)
        else:
            if dir == 0:
                dir = len(dir_deltas) - 1
            else:
                dir -= 1

        for _ in 1..dist:
            if (row, col) in visited_positions:
                if first_twice.isNone():
                    first_twice = some((row, col))

            visited_positions.incl( (row, col) )

            row += dir_deltas[dir][0]
            col += dir_deltas[dir][1]

    echo "row: ", row, " - col: ", col
    echo ">>> part1: ", abs(row)+abs(col)

    echo "twice visited: ", first_twice
    let first_unwrap = first_twice.get()
    echo ">>> part2: ", (abs(first_unwrap[0]) + abs(first_unwrap[1]))

main()
