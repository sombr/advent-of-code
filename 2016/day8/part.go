package main

import "fmt"
import "io"
import "os"
import "strings"
import "strconv"

func throwif(err error) {
    if err != nil {
        panic(err)
    }
}

func rotateRow(s [][]byte, r int) {
    last := len(s[r]) - 1
    prev := s[r][last]
    for c := 0; c < len(s[r]); c++ {
        tmp := s[r][c]
        s[r][c] = prev

        prev = tmp
        last = (last + 1) % len(s[r])
    }
}

func rotateCol(s [][]byte, c int) {
    last := len(s) - 1
    prev := s[last][c]
    for r := 0; r < len(s); r++ {
        tmp := s[r][c]
        s[r][c] = prev

        prev = tmp
        last = (last + 1) % len(s)
    }
}

func apply(s [][]byte, l string) {
    if strings.HasPrefix(l, "rect") {
        parts := strings.Split(l[5:], "x")
        w, err := strconv.Atoi(parts[0])
        throwif(err)
        h, err := strconv.Atoi(parts[1])
        throwif(err)

        for r := 0; r < h; r++ {
            for c := 0; c < w; c++ {
                s[r][c] = 1
            }
        }
        return
    }

    if strings.HasPrefix(l, "rotate row") {
        parts := strings.Split(l[13:], " by ")
        r, err := strconv.Atoi(parts[0])
        throwif(err)
        n, err := strconv.Atoi(parts[1])
        throwif(err)

        for idx := 0; idx < n; idx++ {
            rotateRow(s, r)
        }
    }

    if strings.HasPrefix(l, "rotate column") {
        parts := strings.Split(l[16:], " by ")
        c, err := strconv.Atoi(parts[0])
        throwif(err)
        n, err := strconv.Atoi(parts[1])
        throwif(err)

        for idx := 0; idx < n; idx++ {
            rotateCol(s, c)
        }
    }
}

func main() {
    screen := make([][]byte, 6)
    for r := 0; r < len(screen); r++ {
        screen[r] = make([]byte, 50)
    }

    file, err := os.Open(os.Args[1])
    throwif(err)
    defer file.Close()

    content, err := io.ReadAll(file)
    throwif(err)
    lines := strings.Split(string(content), "\n")

    for _, line := range lines {
        apply(screen, line)
    }

    lit := 0
    for r := 0; r < len(screen); r++ {
        for c := 0; c < len(screen[r]); c++ {
            if screen[r][c] > 0 {
                lit++
            }
        }
    }

    fmt.Println("part1 >>", lit)

    for r := 0; r < len(screen); r++ {
        for c := 0; c < len(screen[r]); c++ {
            if screen[r][c] > 0 {
                fmt.Print("#")
            } else {
                fmt.Print(" ")
            }
        }
        fmt.Println()
    }
}
