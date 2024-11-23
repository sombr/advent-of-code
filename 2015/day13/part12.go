package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

func throwif(err error) {
	if err != nil {
		panic(err)
	}
}

func parseCost(lines []string) map[string]map[string]int {
	res := make(map[string]map[string]int)

	for _, line := range lines {
		if len(line) == 0 {
			break
		}

		parts := strings.Split(line, " ")
		name := parts[0]
		target := parts[ len(parts) - 1 ]
		target = target[:len(target)-1]

		links, found := res[name] // name
		if !found {
			links = make(map[string]int)
		}
		res[name] = links

		change, err := strconv.Atoi(parts[3])
		throwif(err)
		if parts[2] == "lose" {
			change = -change
		}

		links[target] = change
	}

	return res
}

func costMatrix(cost map[string]map[string]int) [][]int {
	var res [][]int = make([][]int, len(cost))
	for idx := 0; idx < len(cost); idx++ {
		res[idx] = make([]int, len(cost))
	}

	name2id := make(map[string]int)
	for name, links := range cost {
		_, found := name2id[name]
		if !found {
			name2id[name] = len(name2id)
		}
		for target, cost := range links {
			_, found := name2id[target]
			if !found {
				name2id[target] = len(name2id)
			}

			res[ name2id[name] ][ name2id[target] ] = cost
		}
	}

	return res
}

func addYourself(cost [][]int) [][]int {
	for idx := 0; idx < len(cost); idx++ {
		cost[idx] = append(cost[idx], 0)
	}
	cost = append(cost, make([]int, len(cost)+1))
	return cost
}

func backtrack(cost [][]int, current_idx int, current_cost int, best_cost int, first_idx int) int {
	cost[current_idx][current_idx] = -1

	var didMove bool = false
	for idx := 0; idx < len(cost); idx++ {
		if cost[idx][idx] < 0 {
			continue
		}

		didMove = true
		cost_change := cost[current_idx][idx] + cost[idx][current_idx]
		path_cost := backtrack(cost, idx, current_cost + cost_change, best_cost, first_idx)

		if path_cost > best_cost {
			best_cost = path_cost
		}
	}

	cost[current_idx][current_idx] = 0

	if !didMove {
		cost_change := cost[first_idx][current_idx] + cost[current_idx][first_idx]
		current_cost += cost_change

		if current_cost > best_cost {
			best_cost = current_cost
		} 
	}
	return best_cost
}

func main() {
	var lines []string

	{
		file, err := os.Open(os.Args[1])
		defer file.Close()
		throwif(err)

		data, err := io.ReadAll(file)
		throwif(err)

		lines = strings.Split(string(data), "\n")
	}

	cost := parseCost(lines)
	fmt.Printf(">>> %+v\n", cost)

	costm := costMatrix(cost)
	fmt.Printf(">>> %+v\n", costm)

	part1 := backtrack(costm, 0, 0, 0, 0)
	fmt.Printf("part1 >>> %d\n", part1)

	cost2 := addYourself(costm)
	part2 := backtrack(cost2, 0, 0, 0, 0)
	fmt.Printf("part2 >>> %d\n", part2)
}