package main

import "fmt"
import "os"
import "io"
import "bytes"

type Field [][]byte

func throwif(err error) {
    if err != nil {
        panic(err)
    }
}

func (f Field) String() string {
    return string(bytes.Join(f, []byte{'\n'}))
}

func findRobot(field [][]byte) (int, int) {
    for ridx, row := range field {
        for cidx, val := range row {
            if val == '@' {
                return ridx, cidx
            }
        }
    }
    return -1, -1
}

func readInput(filename string) (Field, string) {
    var field Field = make([][]byte, 0)
    var moves [][]byte = make([][]byte, 0)

    file, err := os.Open(filename)
    throwif(err)
    defer file.Close()

    content, err := io.ReadAll(file)
    throwif(err)

    lines := bytes.Split(content, []byte("\n"))

    readingMap := true
    for _, line := range lines {
        if len(line) == 0 {
            readingMap = false
            continue
        }

        line = bytes.TrimSpace(line)
        if readingMap {
            field = append(field, line)
        } else {
            moves = append(moves, line)
        }
    }

    return field, string(bytes.Join(moves, []byte{}))
}

// returns new position
func makeMove(field [][]byte, r int, c int, move byte) (int, int) {
    dr := 0
    dc := 0

    switch move {
        case '^': dr = -1
        case 'v': dr = 1
        case '>': dc = 1
        case '<': dc = -1
    }

    nr := r + dr
    nc := c + dc

    if nr < 0 || nc < 0 || nr >= len(field) || nc >= len(field[0]) {
        return r, c
    }

    if field[nr][nc] == '#' { // wall
        return r, c
    }

    if field[nr][nc] == '.' {
        field[r][c], field[nr][nc] = field[nr][nc], field[r][c]
        return nr, nc
    }

    if field[nr][nc] == 'O' {
        // find if there's an empty space
        er := nr
        ec := nc
        for er >= 0 && ec >= 0 && er < len(field) && ec < len(field[0]) {
            switch field[er][ec] {
                case '#': return r, c // no move
                case 'O':
                    // carry on
                    er += dr
                    ec += dc
                    continue
                case '.':
                    field[er][ec], field[nr][nc], field[r][c] = field[nr][nc], field[r][c], field[er][ec]
                    return nr, nc
            }
        }
    }

    return r, c
}

func calcGPS(field [][]byte) int {
    res := 0
    for ridx, row := range field {
        for cidx, val := range row {
            if val == 'O' {
                res += ridx * 100 + cidx
            }
        }
    }

    return res
}

func main() {
    field, moves := readInput(os.Args[1])
    r, c := findRobot(field)

    fmt.Println(field)
    fmt.Println(moves)
    fmt.Println(r, c)

    for _, move := range moves {
        r, c = makeMove(field, r, c, byte(move))
    }

    fmt.Println(field)

    part1 := calcGPS(field)
    fmt.Println("part1 >> ", part1)
}
