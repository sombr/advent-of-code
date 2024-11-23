package main

import (
	"fmt"
)

func main() {
	times := 50
	puzzle_input := "1113222113"

	for idx := 0; idx < times; idx++ {
		puzzle_input = lookAndSay(puzzle_input)
	}

	fmt.Println("part 2 len >>> ", len(puzzle_input))
}