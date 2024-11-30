package main

import (
	"crypto/md5"
	"fmt"
	"io"
	"strings"
)

const INPUT string = "cxdnnyjw"

func find_code(input string) string {
	h := md5.New()

	salt := 0
	code := make([]byte, 0, 8)
	for len(code) < 8 {
		in := fmt.Sprintf("%s%d", input, salt)
		io.WriteString(h, in)
		hash := fmt.Sprintf("%x", h.Sum(nil))

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
	var found byte = 0
	foundCount := 0

	for found != 255 {
		in := fmt.Sprintf("%s%d", input, salt)
		io.WriteString(h, in)
		hash := fmt.Sprintf("%x", h.Sum(nil))

		if strings.HasPrefix(hash, "00000") {
			if hash[5] >= '0' && hash[5] < '8' {
				idx := hash[5] - '0'
				isFound := (found & (1 << idx)) != 0
				if !isFound {
					found = found | (1 << idx)
					code[idx] = hash[6]
					foundCount++
					//fmt.Printf("found: %d at salt: %d -- code:%v, hash:%s mask:%d\n", foundCount, salt, code, hash, found)
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