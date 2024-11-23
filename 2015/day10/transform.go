package main

import (
	"fmt"
	"strings"
)

func lookAndSay(input string) string {
	if len(input) == 0 {
		return ""
	}

	result := make([]string, 0, len(input))

	var count uint32 = 1
	var prev byte = input[0]
	
	for idx := 1; idx < len(input); idx++ {
		if input[idx] != prev {
			result = append(result, fmt.Sprintf("%d%c", count, prev))
			count = 0
			prev = input[idx]
		}
		count++
	}
	result = append(result, fmt.Sprintf("%d%c", count, prev))

	return strings.Join(result, "")
}