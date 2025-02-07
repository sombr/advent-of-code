package main

import "fmt"
import "io"
import "strconv"
import "hash"
import "crypto/md5"

const SALT string = "ihaygndm"
//const SALT string = "abc"

// Part1
func getShortHash(h hash.Hash, index int) []byte {
  h.Reset()
  io.WriteString(h, SALT)
  io.WriteString(h, strconv.Itoa(index))
  hash := h.Sum(nil)
  return hash
}

// Part2
func getLongHash(h hash.Hash, index int) []byte {
  h.Reset()
  io.WriteString(h, SALT)
  io.WriteString(h, strconv.Itoa(index))
  hash := h.Sum(nil)

  for idx := 0; idx < 2016; idx++ {
    h.Reset()
    io.WriteString(h, fmt.Sprintf("%x", hash))
    hash = h.Sum(nil)
  }
  return hash
}

func findIndex(count int) int {
  var three [1001]uint16
  var fives [1001]uint16

  h := md5.New()

  var index int = 0
  var foundKeys int = 0

  for foundKeys < count {
    hash := getLongHash(h, index)

    var c3 byte = 0b111111
    var c5 uint16 = 0

    var idx int = 14 // md5 hash size is 128bit => 16 byte
    for idx >= 0 {
      p := hash[idx] & 0b1111
      match := (p << 4) | p

      if (hash[idx+1] ^ match) == 0 {
        c3 = p
        if idx < 14 && (hash[idx+2] ^ match) == 0 {
          c5 = c5 | (1<<p)
        }
      }

      if (hash[idx] & 0b1111) ^ (hash[idx] >> 4) != 0 {
        idx--
        continue
      }

      p = hash[idx] >> 4
      full_match := hash[idx+1] ^ hash[idx]
      if full_match >> 4 == 0 {
        c3 = p
        if idx < 14 && (full_match == 0) && (hash[idx+2] ^ hash[idx]) >> 4 == 0 {
          c5 = c5 | (1<<p)
        }
      }

      idx--
    }

    rridx := index % len(three)
    fives[rridx] = c5
    if c3 < 0b111111 {
      three[rridx] = 1 << c3
    } else {
      three[rridx] = 0
    }

    // check if key
    rrcan := (rridx + 1) % len(three)
    tval := three[rrcan]
    if tval != 0 {
      for cc := 0; cc < len(fives); cc++ {
        if cc == rrcan {
          continue
        }
        if fives[cc] & tval != 0 {
          foundKeys++
          break
        }
      }
    }


    index++
  }
  return index - len(three)
}

func main() {
  fmt.Println("Key index >> ", findIndex(64))
}
