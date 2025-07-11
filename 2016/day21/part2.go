package main

import "os"
import "io"
import "strings"
import "bytes"
import "strconv"
import "fmt"
import "slices"

type Str []byte

func (s Str) SwapAtIndex(x, y int) {
    s[x], s[y] = s[y], s[x]
}

func (s Str) SwapLetters(x, y byte) {
    for idx := 0; idx < len(s); idx++ {
        if s[idx] == x || s[idx] == y {
            if s[idx] == x {
                s[idx] = y
            } else {
                s[idx] = x
            }
        }
    }
}

func (s Str) Rotate(steps int) {
    var tmp []byte = make([]byte, len(s))

    start := steps
    if start < 0 {
        start += len(s)
    }

    for idx := 0; idx < len(s); idx++ {
        tmp[ (start+idx) % len(s) ] = s[idx]
    }

    copy(s, tmp)
}

func (s Str) RotateByte(b byte) {
    idx := bytes.IndexByte(s, b)
    if idx < 0 {
        panic("cannot find")
    }

    steps := 1 + idx
    if idx >= 4 {
        steps++
    }

    s.Rotate(steps)
}

func (s Str) Reverse(x, y int) {
    for x < y {
        s.SwapAtIndex(x, y)
        x++
        y--
    }
}

func (s Str) Move(x, y int) {
    if x == y {
        return
    }

    tmp := s[x]

    step := 1
    if y < x {
        step = -1
    }

    for idx := x; idx != y; idx += step {
        s[idx] = s[idx+step]
    }
    s[y] = tmp
}

func ReadInput(filename string) []string {
    file, err := os.Open(filename)
    if err != nil {
        panic(err)
    }
    defer file.Close()

    content, err := io.ReadAll(file)
    if err != nil {
        panic(err)
    }

    return strings.Split(string(content), "\n")
}

func main() {
    filename := os.Args[1]

    lines := ReadInput(filename)
    slices.Reverse(lines)

    str := Str([]byte("fbgdceah"))

    for _, line := range lines {
        parts := strings.Fields(line)
        if strings.HasPrefix(line, "swap position") {
            x, _ := strconv.Atoi(parts[2])
            y, _ := strconv.Atoi(parts[5])

            str.SwapAtIndex(x, y)
            fmt.Printf("swapped pos %d and %d, new string: %s\n", x, y, string(str))
            
            continue
        }

        if strings.HasPrefix(line, "swap letter") {
            x := parts[2]
            y := parts[5]

            str.SwapLetters(x[0], y[0])
            fmt.Printf("swapped letters %s and %s, new string: %s\n", x, y, string(str))

            continue
        }

        if strings.HasPrefix(line, "reverse") {
            x, _ := strconv.Atoi(parts[2])
            y, _ := strconv.Atoi(parts[4])

            str.Reverse(x, y)
            fmt.Printf("reverse from %d to %d, new string: %s\n", x, y, string(str))

            continue
        }

        if strings.HasPrefix(line, "rotate based") {
            b := parts[6]

            valid := make([]int, 0)
            for idx := 0; idx < len(str); idx++ {
                prev := Str(make([]byte, len(str)))
                copy(prev, str)

                prev.Rotate(idx)
                prev.RotateByte(b[0])

                if bytes.Equal(str, prev) {
                    fmt.Printf("valid rotation idx: %d\n", idx)
                    valid = append(valid, idx)
                }
            }

            if len(valid) == 1 {
                str.Rotate(valid[0])
                fmt.Printf("unrotated based on %s, steps: %d, new string: %s\n", b, valid[0], string(str))
            } else {
                panic("unknown rotation")
            }

            continue
        }

        if strings.HasPrefix(line, "rotate") {
            dir := -1
            if parts[1] == "left" {
                dir = 1
            }

            steps, _ := strconv.Atoi(parts[2])

            str.Rotate(dir*steps)
            fmt.Printf("rotated steps: %d, new string: %s\n", steps, string(str))

            continue
        }

        if strings.HasPrefix(line, "move") {
            x, _ := strconv.Atoi(parts[2])
            y, _ := strconv.Atoi(parts[5])

            str.Move(y, x)
            fmt.Printf("moves pos %d to %d, new string: %s\n", x, y, string(str))

            continue
        }
    }
}
