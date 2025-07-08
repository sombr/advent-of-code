def find_allowed(rs)
  idx = 0.to_i64()

  first = nil
  allowed = 0.to_i64()
  while rs.size() > 0 && idx <= 4294967295
    printf(">> idx:%d rs[0]: %d-%d\n", idx, rs[0][0], rs[0][1])
    if idx > rs[0][1]
      rs.shift()
      next
    end

    if idx < rs[0][0]
      if first == nil
        first = idx
      end
      allowed += 1
    else
      idx = rs[0][1]
    end

    idx += 1
  end

  allowed += 4294967295 - idx + 1

  return first, allowed
end

def main(filename)
  ranges = [] of Array(Int64)

  File.each_line(filename, chomp: true) do |line|
    from, to = line.split("-")
    from = from.to_i64()
    to = to.to_i64()

    ranges.push( [from, to] )
  end

  ranges.sort!()

  first, count = find_allowed(ranges)
  print(first, " ", count, "\n")
end

main(ARGV[0])
