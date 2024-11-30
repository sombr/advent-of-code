package main

import "fmt"
import "io"
import "os"
import "strings"

func throwif(err error) {
    if err != nil {
        panic(err)
    }
}

func checkIfGood(ls string) bool {
    bracket := 0
    window := []byte{ 0, 0, 0, 0 }
    widx := 0

    foundAbba := false
    for _, l := range ls {
        if l == '[' {
            bracket++
            window = []byte{ 0, 0, 0, 0 }
            widx = 0
            continue
        }
        if l == ']' {
            bracket--
            window = []byte{ 0, 0, 0, 0 }
            widx = 0
            continue
        }

        window[widx] = byte(l)
        widx = (widx + 1) % len(window)

        w1 := widx
        w2 := (widx + 1) % len(window)
        w3 := (widx + 2) % len(window)
        w4 := (widx + 3) % len(window)
        
        if window[w1] == window[w4] && window[w2] == window[w3] && window[w1] != window[w2] {
            if bracket > 0 {
                return false
            }
            foundAbba = true
        }
    }

    return foundAbba
}

func checkIfGood2(ls string) bool {
    bracket := 0
    window := []byte{ 0, 0, 0 }
    widx := 0

    foundIn := make(map[string]int)
    foundOut := make(map[string]int)
    for _, l := range ls {
        if l == '[' {
            bracket++
            window = []byte{ 0, 0, 0 }
            widx = 0
            continue
        }
        if l == ']' {
            bracket--
            window = []byte{ 0, 0, 0 }
            widx = 0
            continue
        }

        window[widx] = byte(l)
        widx = (widx + 1) % len(window)

        w1 := widx
        w2 := (widx + 1) % len(window)
        w3 := (widx + 2) % len(window)
        
        if window[w1] == window[w3] && window[w1] != window[w2] {
            if bracket > 0 {
                reverse := fmt.Sprintf("%c%c%c", window[w2], window[w1], window[w2])
                foundIn[reverse] = 1
                if foundOut[reverse] > 0 {
                    return true
                }
            } else {
                straight := fmt.Sprintf("%c%c%c", window[w1], window[w2], window[w1])
                foundOut[straight] = 1
                if foundIn[straight] > 0 {
                    return true
                }
            }
        }
    }

    return false
}

func main() {
    file, err := os.Open(os.Args[1])
    throwif(err)

    content, err := io.ReadAll(file)
    throwif(err)

    lines := strings.Split(string(content), "\n")

    goodLines := 0
    sslLines := 0
    for _, line := range lines {
        isGood := checkIfGood(line)
        if isGood {
            goodLines++
        }
        isSSL := checkIfGood2(line)
        if isSSL {
            sslLines++
        }
    }

    fmt.Println("part1 >>", goodLines)
    fmt.Println("part2 >>", sslLines)
}
