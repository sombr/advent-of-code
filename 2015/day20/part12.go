package main

import (
	"fmt"
	"math"
)

func compute_presents_for_house(house uint32) uint32 {
	var presents uint32 = 0

	// find factors
	for idx := uint32(1); idx <= uint32(math.Ceil(math.Sqrt(float64(house)))); idx++ {
		remainder := house % idx
		if remainder == 0 {
			presents += idx * 10 + (house / idx) * 10
		}
	}

	return presents
}

func compute_presents_for_house2(house uint32) uint32 {
	var presents uint32 = 0

	// find factors
	for idx := uint32(1); idx <= uint32(math.Ceil(math.Sqrt(float64(house)))); idx++ {
		remainder := house % idx
		if remainder == 0 {
			f1 := idx
			f2 := house / idx

			if house / f2 <= 50 {
				presents += f2 * 11
			}
			if house / f1 <= 50 {
				presents += f1 * 11
			}
		}
	}

	return presents
}

func main() {
	var input uint32 = 36_000_000
	var part1 uint32 = 0
	var part2 uint32 = 0

	for idx := uint32(1); idx <= input; idx++ {
		part1 = idx
		if compute_presents_for_house(idx) >= input {
			break;
		}
	}

	fmt.Printf("part1 >> %v\n", part1)

	for idx := uint32(1); idx <= input; idx++ {
		part2 = idx
		if compute_presents_for_house2(idx) >= input {
			break;
		}
	}

	fmt.Printf("part2 >> %v\n", part2)
}