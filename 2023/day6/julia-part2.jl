
function count_winning_times(time::Int64, dist::Int64)::Int64
    D = time^2 - 4 * dist

    # losses or ties
    if D <= 0
        return 0
    end

    println("D: ", D)
    
    range_start = (time - sqrt(D) ) / 2.0
    range_end = (time + sqrt(D) ) / 2.0

    println("roots: [$range_start, $range_end]")

    range_start_int = ceil(range_start)
    range_end_int = floor(range_end)

    println("int roots: ($range_start, $range_end)")
    if Float64(range_start_int) - range_start == 0
        range_start_int += 1
    end
    if Float64(range_end_int) - range_end == 0
        range_end_int -= 1
    end

    return range_end_int - range_start_int + 1
end

function main(filename)
    times = ""
    dists = ""
    open(filename, "r") do io
        (times, dists) = readlines(io)
    end

    times = [ parse(Int64, replace(split(times, ":")[2], " " => "")) ]
    dists = [ parse(Int64, replace(split(dists, ":")[2], " " => "")) ]

    win_counts = [ count_winning_times(p...) for p in zip(times, dists) ]

    println(times, " ", dists, " ", win_counts)

    res = reduce(*, win_counts)
    println("result: ", res)
end

if length(ARGS) < 1
    println("usage: ", PROGRAM_FILE, " < input >")
else
    main(ARGS[1])
end