package main

import "fmt"
import "os"
import "io"
import "bytes"

type Field [][]byte

type Box struct {
    r int
    c int
}

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

func readInput(filename string, expand bool) (Field, string) {
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
            if expand {
                fieldRow := make([]byte, 0)
                for _, sym := range line {
                    switch sym {
                        case '#': fieldRow = append(fieldRow, '#', '#')
                        case 'O': fieldRow = append(fieldRow, '[', ']')
                        case '.': fieldRow = append(fieldRow, '.', '.')
                        case '@': fieldRow = append(fieldRow, '@', '.')
                    }
                }
                field = append(field, fieldRow)
            } else {
                field = append(field, line)
            }
        } else {
            moves = append(moves, line)
        }
    }

    return field, string(bytes.Join(moves, []byte{}))
}

func tryMoveBoxes(field [][]byte, boxes []Box, move byte) bool {
    touchingBoxes := make([]Box, 0)
    for _, box := range boxes {
        switch move {
            case '^':
                nr := box.r - 1
                nc := box.c

                if nr < 0 || field[nr][nc] == '#' || field[nr][nc+1] == '#' {
                    return false
                }

                if field[nr][nc] == '[' {
                    touchingBoxes = append(touchingBoxes, Box{nr, nc})
                }

                if field[nr][nc+1] == '[' {
                    touchingBoxes = append(touchingBoxes, Box{nr, nc+1})
                }

                if field[nr][nc] == ']' {
                    touchingBoxes = append(touchingBoxes, Box{nr, nc-1})
                }
            case 'v':
                nr := box.r + 1
                nc := box.c

                if nr >= len(field) || field[nr][nc] == '#' || field[nr][nc+1] == '#' {
                    return false
                }

                if field[nr][nc] == '[' {
                    touchingBoxes = append(touchingBoxes, Box{nr, nc})
                }

                if field[nr][nc+1] == '[' {
                    touchingBoxes = append(touchingBoxes, Box{nr, nc+1})
                }

                if field[nr][nc] == ']' {
                    touchingBoxes = append(touchingBoxes, Box{nr, nc-1})
                }
            case '>':
                nr := box.r
                nc := box.c + 2

                if nc >= len(field[nr]) || field[nr][nc] == '#' {
                    return false
                }

                if field[nr][nc] == '[' {
                    touchingBoxes = append(touchingBoxes, Box{nr, nc})
                }
            case '<':
                nr := box.r
                nc := box.c - 1

                if nc < 0 || field[nr][nc] == '#' {
                    return false
                }

                if field[nr][nc] == ']' {
                    touchingBoxes = append(touchingBoxes, Box{nr, nc-1})
                }
        }
    }

    if len(touchingBoxes) > 0 {
        unique := make(map[Box]bool)
        for _, box := range touchingBoxes {
            unique[box] = true
        }

        uniqueList := make([]Box, 0, len(unique))
        for box, _ := range unique {
            uniqueList = append(uniqueList, box)
        }

        success := tryMoveBoxes(field, uniqueList, move)
        if !success {
            return false
        }
    }

    for _, box := range boxes {
        r := box.r
        c := box.c
        switch move {
            case '^':
                nr := r-1
                nc := c

                field[r][c], field[nr][nc] = field[nr][nc], field[r][c]
                field[r][c+1], field[nr][nc+1] = field[nr][nc+1], field[r][c+1]
            case 'v':
                nr := r+1
                nc := c

                field[r][c], field[nr][nc] = field[nr][nc], field[r][c]
                field[r][c+1], field[nr][nc+1] = field[nr][nc+1], field[r][c+1]
            case '>':
                field[r][c], field[r][c+1], field[r][c+2] = field[r][c+2], field[r][c], field[r][c+1]
            case '<':
                field[r][c-1], field[r][c], field[r][c+1] = field[r][c], field[r][c+1], field[r][c-1]
        }
    }

    return true
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

    if field[nr][nc] == '[' || field[nr][nc] == ']' {
        box := Box {nr, nc}
        if field[nr][nc] == ']' {
            box.c -= 1
        }
        success := tryMoveBoxes(field, []Box{ box }, move)
        if success {
            field[r][c], field[nr][nc] = field[nr][nc], field[r][c]
            return nr, nc
        }
        return r, c
    }

    return r, c
}

func calcGPS(field [][]byte) int {
    res := 0
    for ridx, row := range field {
        for cidx, val := range row {
            if val == '[' {
                res += ridx * 100 + cidx
            }
        }
    }

    return res
}

func checkBroken(field [][]byte) bool {
    for _, row := range field {
        for cidx, val := range row {
            if val == ']' && cidx > 0 && row[cidx-1] != '[' {
                return true
            }
        }
    }
    return false
}

func main() {
    field, moves := readInput(os.Args[1], true)
    r, c := findRobot(field)

    fmt.Println(field)
    fmt.Println(moves)
    fmt.Println(r, c)

    for _, move := range moves {
        r, c = makeMove(field, r, c, byte(move))
    }

    part2 := calcGPS(field)
    fmt.Println("part2 >> ", part2)
}
