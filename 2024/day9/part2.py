filename = "input.txt"

def print_disk(disk):
  for bid, span in disk:
    sym = str(bid) if bid >= 0 else '.'
    for _ in range(span):
      print(sym, end="")
      
  print()

def main():
  disk = []
  with open(filename, "r") as file:
    line = file.readline().strip()
    
    fileid = 0
    for idx, b in enumerate(line):
      span = ord(b) - ord('0')
      blockid = -1
      if idx % 2 == 0:
        blockid = fileid
        fileid += 1
      disk.append( (blockid, span) )
    
  # try to fit
  idx = len(disk)-1
  while idx > 0:
    # print_disk(disk)
    
    bid, span = disk[idx]
    if bid < 0:
      idx -= 1
      continue
      
    # find left-most span
    for edx in range(idx):
      eid, espan = disk[edx]
      if eid >= 0:
        continue
      delta = espan - span
      if delta >= 0:
        disk[edx] = (-1, delta)
        disk[idx] = (-1, span)
        disk.insert( edx, (bid, span) )
        idx += 1
        break
    
    idx -= 1
    
  # when done
  checksum = 0
  idx = 0
  for bid, span in disk:
    for _ in range(span):
      if bid >= 0:
        checksum += idx * bid
      idx += 1
      
  print(f"part2 {checksum}")
    
main()
