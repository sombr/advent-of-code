
package main

import "fmt"
import "os"
import "io"

func throwif(err error) {
    if err != nil {
        panic(err)
    }
}

type Iterator interface {
    hasNext() bool
    next() (int, int)
}

type DiskIterator struct {
    spanIterators []Iterator
    currentSpan int
    forward bool
}

func NewDiskIterator(data []byte, forward bool) *DiskIterator {
    spans := make([]Iterator, 0, len(data))
    fileId := 0
    startPosition := 0

    for idx, span := range data {
        blockId := -1
        if idx % 2 == 0 {
            blockId = fileId
        }

        spans = append(spans, NewSpanIterator(
            blockId, int(span), int(startPosition), forward,
        ))

        if idx % 2 == 0 {
            fileId++
        }
        startPosition += int(span)
    }
    return &(DiskIterator {
        spanIterators: spans,
        currentSpan: 0,
        forward: forward,
    })
}

func (di *DiskIterator) hasNext() bool {
    for di.currentSpan < len(di.spanIterators) && !di.currentIter().hasNext() {
        di.currentSpan++
    }
    return di.currentSpan < len(di.spanIterators) && di.currentIter().hasNext()
}

func (di *DiskIterator) currentIter() Iterator {
    pos := di.currentSpan
    if !di.forward {
        pos = len(di.spanIterators) - pos - 1
    }

    return di.spanIterators[pos]
}

func (di *DiskIterator) next() (int, int) {
    for !di.currentIter().hasNext() {
        di.currentSpan++
    }

    return di.currentIter().next()
}

type SpanIterator struct {
    fileId int
    blockClount int
    currentBlock int

    startPosition int
    forward bool
}

func NewSpanIterator(fileId int, blocks int, startPosition int, forward bool) *SpanIterator {
    return &(SpanIterator {
        fileId: fileId,
        blockClount: blocks,
        currentBlock: 0,
        startPosition: startPosition,
        forward: forward,
    })
}

func (si *SpanIterator) hasNext() bool {
    return si.currentBlock < si.blockClount
}

func (si *SpanIterator) next() (int, int) {
    pos := si.startPosition + si.currentBlock
    if !si.forward {
        pos = si.startPosition + si.blockClount - si.currentBlock - 1
    }

    si.currentBlock++

    return pos, si.fileId
}

func main() {
    file, err := os.Open(os.Args[1])
    throwif(err)
    defer file.Close()

    blocks, err := io.ReadAll(file)
    throwif(err)

    var totalSpace int = 0
    for idx := range blocks {
        if blocks[idx] >= '0' && blocks[idx] <= '9' {
            blocks[idx] -= '0'
        } else {
            blocks = blocks[:idx]
            break
        }
        totalSpace += int(blocks[idx])
    }

    var forward Iterator = NewDiskIterator(blocks, true)
    var reverse Iterator = NewDiskIterator(blocks, false)

    lpos := 0
    rpos := totalSpace - 1

    lval := 0
    rval := 0

    checksum := 0
    for forward.hasNext() && reverse.hasNext() && lpos < rpos-1 {
        lpos, lval = forward.next()

        if lval >= 0 {
            checksum += lval * lpos
        } else {
            for {
                rpos, rval = reverse.next()
                if rpos <= lpos {
                    break
                }
                if rval >= 0 {
                    break
                }
            }
            checksum += rval * lpos
        }
    }

    fmt.Println("part1 >> ", checksum)
}
