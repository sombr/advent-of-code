package main

import "fmt"
import "os"
import "io"
import "bytes"
import "strconv"
import "math"

type Range struct {
    start int
    end int
}

func btoi(s []byte) int {
    num, err := strconv.Atoi(string(s))
    if err != nil {
        panic(err)
    }
    return num
}

func main() {
    filename := os.Args[1]
    file, _ := os.Open(filename)
    defer file.Close()

    input := make([]Range, 0)

    data, _ := io.ReadAll(file)
    data = bytes.TrimSpace(data)
    lines := bytes.Split(data, []byte{','})

    for _, line := range lines {
        parts := bytes.Split(line, []byte{'-'})
        input = append(input, Range {
            start: btoi(parts[0]),
            end: btoi(parts[1]),
        })
    }

    solution1 := part1(input)
    solution2 := part2(input)

    fmt.Printf("solution 1: %d\nsolution 2: %d\n", solution1, solution2)
}

func findClosestPowerOfTen(n int) int {
    return int(math.Log10(float64(n)))
}

func validateNumber(n int) bool {
    power := findClosestPowerOfTen(n)
    if power % 2 == 0 {
        return false
    }

    divider := int(math.Pow10(power/2+1) + 1)
    return (n % divider) == 0
}

func part1(input []Range) uint64 {
    var sum uint64 = 0
    for _, r := range input { 
        for n := r.start; n <= r.end; n++ {
            v := validateNumber(n)
            if v {
                sum += uint64(n)
            }
        }
    }

    return sum
}

func part2(input []Range) uint64 {
    return 1
}
