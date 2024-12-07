package main

import "fmt"
import "os"
import "io"
import "strings"
import "strconv"
import "slices"

func throwif(err error) {
    if err != nil {
        panic(err)
    }
}

type Equation struct {
    Result uint64
    Components []uint64
}

type Op func(uint64, uint64) uint64

func backtrack(target uint64, cs []uint64, csize int, ops []Op) bool {
    if csize == 0 {
        return false
    }
    if csize == 1 {
        return target == cs[0]
    }

    b := cs[ csize - 2 ]
    a := cs[ csize - 1 ]

    for _, op := range ops {
        c := op(a, b)
        cs[ csize - 2 ] = c

        check := backtrack(target, cs, csize - 1, ops)

        cs[ csize - 2 ] = b

        if check {
            return true
        }
    }

    return false
}

func CheckComposable(eq Equation, ops []Op) bool {
    return backtrack(eq.Result, eq.Components, len(eq.Components), ops)
}

func ProcessEquations(es []Equation, ops []Op) uint64 {

    calibrationResult := uint64(0)
    for _, eq := range es {
        isComposable := CheckComposable(eq, ops)
        if isComposable {
            calibrationResult += eq.Result
        }
    }

    return calibrationResult
}

func main() {
    file, err := os.Open(os.Args[1])
    throwif(err)
    defer file.Close()

    raw, err := io.ReadAll(file)
    throwif(err)

    lines := strings.Split(strings.TrimSpace(string(raw)), "\n")
    input := make([]Equation, 0, len(lines))

    for _, line := range lines {
        line = strings.TrimSpace(line)
        if len(line) == 0 {
            continue
        }

        parts := strings.Split(line, ":")
        cparts := strings.Fields(parts[1])

        result, err := strconv.Atoi( strings.TrimSpace(parts[0]) )
        throwif(err)

        components := make([]uint64, 0, len(cparts))
        for _, cp := range cparts {
            component, err := strconv.Atoi(cp)
            throwif(err)

            components = append(components, uint64(component))
        }
        slices.Reverse(components) // -- because I need a front-ordered stack

        input = append(input, Equation { Result: uint64(result), Components: components })
    }

    // part 1
    var ops []Op = []Op{
        func (a uint64, b uint64) uint64 { return a + b },
        func (a uint64, b uint64) uint64 { return a * b },
    }
    calibrationResult := ProcessEquations(input, ops)
    fmt.Printf(">> part1: %d\n", calibrationResult)

    ops = append(ops, func (a uint64, b uint64) uint64 {
        mag := uint64(1)
        for mag <= b  {
            mag *= 10
        }
        return a*mag + b
    })
    calibrationResult = ProcessEquations(input, ops)
    fmt.Printf(">> part2: %d\n", calibrationResult)
}
