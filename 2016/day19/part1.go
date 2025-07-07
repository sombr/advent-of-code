package main

import "fmt"

func main() {
    count := 3014387

    gifts := make([]uint64, count)
    nexts := make([]int, count)

    for idx := 0; idx < count; idx++ {
        gifts[idx] = 1
        nexts[idx] = (idx+1) % count
    }

    cur := 0
    for cur != nexts[cur] && gifts[nexts[cur]] > 0 {
        next := nexts[cur]

        nexts[cur] = nexts[next]
        gifts[cur] += gifts[next]
        gifts[next] = 0

        cur = nexts[next]
        nexts[next] = -1
    }

    fmt.Printf(">>> result position: %d, with gifts: %d\n", cur+1, gifts[cur])
}
