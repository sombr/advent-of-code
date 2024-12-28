package main

import "fmt"
import "os"
import "io"
import "sort"
import "strings"

type Cell struct {
    r int
    c int
    direction string
}

type CellSet map[Cell]bool

func throwif(err error) {
    if err != nil {
        panic(err)
    }
}

func showField(field [][]rune) string {
    rows := make([]string, 0)
    for _, row := range field {
        rows = append(rows, string(row))
    }
    return strings.Join(rows, "\n")
}

func loadData(filename string) [][]rune {
    file, err := os.Open(filename)
    throwif(err)

    defer file.Close()

    content, err := io.ReadAll(file)
    throwif(err)

    scontent := strings.TrimSpace( string(content) )

    field := make([][]rune, 0)
    for _, line := range strings.Split(scontent, "\n") {
        field = append(field, []rune(line))
    }

    return field
}

func vec2idx(rows int, r int, c int) int {
    return rows * c + r
}

func idx2vec(rows int, idx int) (int, int) {
    c := idx / rows
    r := idx % rows
    return r, c
}

func makeComponentField(rows int, cols int) [][]int {
    field := make([][]int, 0)
    for r := 0; r < rows; r++ {
        row := make([]int, 0)
        for c := 0; c < cols; c++ {
            row = append(row, vec2idx(rows, r, c))
        }
        field = append(field, row)
    }

    return field
}

func findComponent(field [][]int, r int, c int) int {
    rows := len(field)

    idx := vec2idx(rows, r, c)
    if field[r][c] != idx {
        rn, cn := idx2vec(rows, field[r][c])
        idx = findComponent(field, rn, cn)
    }

    field[r][c] = idx

    return idx
}

func unionComponents(field [][]int, r1 int, c1 int, r2 int, c2 int) {
    v1 := findComponent(field, r1, c1)
    v2 := findComponent(field, r2, c2)

    v1r, v1c := idx2vec(len(field), v1)
    v2r, v2c := idx2vec(len(field), v2)

    if v1 < v2 {
        field[v2r][v2c] = v1
    } else {
        field[v1r][v1c] = v2
    }
}

func delta(yield func(int, int) bool) {
    for _, dr := range []int{-1, 0, 1} {
        for _, dc := range []int{-1, 0, 1} {
            if dr == 0 && dc == 0 {
                continue
            }
            if dr != 0 && dc != 0 {
                continue
            }

            yield(dr, dc)
        }
    }
}

func findShapes(data [][]rune, field [][]int) {
    for r := 0; r < len(data); r++ {
        for c := 0; c < len(data[r]); c++ {
            for dr, dc := range delta {
                nr := r + dr
                nc := c + dc

                if nr < 0 || nc < 0 || nr >= len(data) || nc >= len(data[r]) {
                    continue
                }

                if data[r][c] == data[nr][nc] {
                    unionComponents(field, r, c, nr, nc)
                }
            }
        }
    }
}

func collectShapes(field [][]int) map[int]CellSet {
    res := make(map[int]CellSet)

    for r := 0; r < len(field); r++ {
        for c := 0; c < len(field[r]); c++ {
            shape, found := res[ field[r][c] ]
            if !found {
                shape = make(CellSet)
            }

            cell := Cell { r: r, c: c }
            shape[cell] = true
            res[ field[r][c] ] = shape
        }
    }

    return res
}

func findEdges(shape CellSet) []Cell {
    res := make([]Cell, 0)

    for cell, _ := range shape {
        for dr, dc := range delta {
            nr := cell.r + dr
            nc := cell.c + dc

            neighbour := Cell { r: nr, c: nc }
            _, inShape := shape[neighbour]

            if inShape {
                continue
            }

            if dr == -1 {
                neighbour.direction = "^"
            }
            if dr == 1 {
                neighbour.direction = "v"
            }
            if dc == -1 {
                neighbour.direction = "<"
            }
            if dc == 1 {
                neighbour.direction = ">"
            }

            res = append(res, neighbour)
        }
    }

    return res
}

func sortEdges(res []Cell, byRow bool) {

    sort.Slice(res, func (i int, j int) bool {
        sameRow := res[i].r == res[j].r
        sameCol := res[i].c == res[j].c

        if res[i].direction == res[j].direction {
            if byRow {
                if sameRow {
                    return res[i].c < res[j].c
                }
                return res[i].r < res[j].r
            } else {
                if sameCol {
                    return res[i].r < res[j].r
                }
                return res[i].c < res[j].c
            }
        }

        return res[i].direction < res[j].direction
    })

}

func countEdges(cells []Cell) int {
    if len(cells) == 0 {
        return 0
    }

    horizontal := make([]Cell, 0)
    vertical := make([]Cell, 0)

    for _, cell := range cells {
        if cell.direction == "^" || cell.direction == "v" {
            horizontal = append(horizontal, cell)
        } else {
            vertical = append(vertical, cell)
        }
    }

    sortEdges(horizontal, true)
    sortEdges(vertical, false)

    edges := 0

    if len(horizontal) > 0 {
        edges++
        for idx, cell := range horizontal {
            if idx == 0 {
                continue
            }

            prev := horizontal[idx-1]
            if cell.r != prev.r || cell.direction != prev.direction || cell.c - prev.c > 1 {
                edges++
            }
        }
    }

    if len(vertical) > 0 {
        edges++
        for idx, cell := range vertical {
            if idx == 0 {
                continue
            }

            prev := vertical[idx-1]
            if cell.c != prev.c || cell.direction != prev.direction || cell.r - prev.r > 1 {
                edges++
            }
        }
    }

    return edges
}

func getShapeTag(data [][]rune, shape CellSet) string {
    for cell, _ := range shape {
        return string(data[cell.r][cell.c])
    }
    return ""
}

func main() {
    data := loadData(os.Args[1])

    rows := len(data)
    cols := len(data[0])

    coms := makeComponentField(rows, cols)

    fmt.Println(coms)

    findShapes(data, coms)

    fmt.Println(coms)

    shapes := collectShapes(coms)

    fmt.Println(shapes)

    totalCost := 0
    for _, shape := range shapes {
        tag := getShapeTag(data, shape)
        area := len(shape)
        edges := findEdges(shape)
        ecount := countEdges(edges)
        fmt.Println(tag, " >>> ", area, "x", ecount, "=", area*ecount)

        totalCost += area*ecount
    }

    fmt.Println("part2 >> ", totalCost)
}
