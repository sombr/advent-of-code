package main

import "fmt"
import "strings"

type Player struct {
    index uint32
    presents uint32
    next *Player
    prev *Player
}

func BuildCircle(count int) *Player {
    if count == 0 {
        return nil
    }
    if count == 1 {
        res := &Player {
            index: 1,
            presents: 1,
        }
        res.next = res
        res.prev = res
        return res
    }

    smallLoop := BuildCircle(count - 1)

    extra := &Player {
        index: uint32(count),
        presents: 1,
        next: smallLoop,
        prev: smallLoop.prev,
    }

    smallLoop.prev.next = extra
    smallLoop.prev = extra

    return smallLoop
}

func (p *Player) String() string {
    parts := make([]string, 0)

    cur := p
    for {
        parts = append(parts, fmt.Sprintf("[id:%d v:%d <:%d >:%d]",
            cur.index, cur.presents, cur.prev.index, cur.next.index))
        cur = cur.next
        if cur == nil || cur == p {
            break
        }
    }
    return strings.Join(parts, " -> ")
}

func StealAndRemove(start *Player, count int) *Player {
    if count == 1 {
        return start
    }
    if count % 100 == 0 {
        fmt.Printf(">> loop len: %d\n", count)
    }

    offset := count / 2
    stealer := start

    for idx := 0; idx < offset; idx++ {
        stealer = stealer.next
    }

    //fmt.Printf(">> found for stealing: %+v\n", *stealer)

    //fmt.Printf(">> stealing with %+v from %+v\n", *start, *stealer)
    start.presents += stealer.presents

    stealer.prev.next = stealer.next
    stealer.next.prev = stealer.prev
    stealer.next = nil
    stealer.prev = nil

    //fmt.Printf(">> after stealing: > %s\n", start)

    return StealAndRemove(start.next, count-1)
}

func main() {
    count := 3014387

    players := BuildCircle(count)

    //fmt.Printf(">> before : %+v\n", players)

    players = StealAndRemove(players, count)

    fmt.Printf(">> after : %+v\n", players)
}
