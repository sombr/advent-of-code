package main

import (
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"io"
	"strconv"
	"strings"
)

const INPUT string = "cxdnnyjw"

func find_code(input string) string {
	h := md5.New()

	salt := 0
	code := make([]byte, 0, 8)
	for len(code) < 8 {
		io.WriteString(h, input)
		io.WriteString(h, strconv.Itoa(salt))

		hash_bin := h.Sum(nil)
		hash := hex.EncodeToString(hash_bin[:3])

		if strings.HasPrefix(hash, "00000") {
			code = append(code, hash[5])
		}

		salt++
		h.Reset()
	}

	return string(code)
}

func find_code2(input string) string {
	h := md5.New()

	salt := 0
	code := make([]byte, 8)
	foundCount := 0

	for foundCount < 8 {
		io.WriteString(h, input)
		io.WriteString(h, strconv.Itoa(salt))

		hash_bin := h.Sum(nil)
		hash := hex.EncodeToString(hash_bin[:4])

		if strings.HasPrefix(hash, "00000") {
			if hash[5] >= '0' && hash[5] < '8' {
				idx := hash[5] - '0'
				if code[idx] == 0 {
					code[idx] = hash[6]
					foundCount++
				}
			}
		}

		salt++
		h.Reset()
	}

	return string(code)
}

func main() {
	fmt.Println("test >>", find_code("abc"))
	fmt.Println("part1 >>", find_code(INPUT))
	fmt.Println("part2 >>", find_code2(INPUT))
}

/*
		Go 1.23.2 GOAMD64=v1

        User time (seconds): 42.17
        System time (seconds): 0.48
        Percent of CPU this job got: 104%

		v2

		User time (seconds): 41.95
        System time (seconds): 0.47
        Percent of CPU this job got: 104%

		v3 + optimizations of string formatting, it looks like they are super slow

		User time (seconds): 19.32
        System time (seconds): 0.17
        Percent of CPU this job got: 103%
*/