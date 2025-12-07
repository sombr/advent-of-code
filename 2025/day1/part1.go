package main

import "io"
import "os"
import "fmt"

func throwif(err error) {
    if err != nil {
        panic(err)
    }
}

func MoveDial(dial int, turns int) int {
    dial += turns
    if dial < 0 {
        dial += 100
    }

    return dial % 100
}

func CountAtZero(timesAtZero int, dial int) int {
    if dial == 0 {
        return timesAtZero + 1
    }
    return timesAtZero
}

func SolvePart1(s []byte) int {
    var direction int = 0
    var number int = 0

    var dial int = 50
    var timesAtZero int = 0

    for idx := 0; idx < len(s); idx++ {
        c := s[idx]

        if c == '\n' { // proceed
            dial = MoveDial(dial, direction*number)
            timesAtZero = CountAtZero(timesAtZero, dial)

            direction = 0
            number = 0
            continue
        }

        if (c & (1<<6)) != 0 { // L or R
            direction = int(1 - int8(((c >> 3) & 1) * 2)) // left -1 or 1
            continue
        }

        // digit
        number = number*10 + int(c - '0')
    }

    if direction != 0 {
        dial = MoveDial(dial, direction*number)
        timesAtZero = CountAtZero(timesAtZero, dial)
    }

    return timesAtZero
}

func LoadInput(filename string) []byte {
    fh, err := os.Open(filename)
    throwif(err)
    defer fh.Close()

    data, err := io.ReadAll(fh)
    throwif(err)

    return data
}

func main() {
    // load data
    filename := os.Args[1]
    data := LoadInput(filename)

    sol1 := SolvePart1(data)
    fmt.Println("part1 :: ", sol1)
}
