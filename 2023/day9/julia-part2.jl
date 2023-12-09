#!/usr/bin/env julia

function get_deltas(xs::Vector{Int32})::Vector{Int32}
    res = []
    for idx in 2:length(xs)
        push!(res, xs[idx] - xs[idx-1])
    end

    return res
end

function steps_to_zeros(xs::Vector{Int32})::Vector{Int32}
    last_elements = []

    cur = xs
    while !all([ x == 0 for x in cur ])
        push!(last_elements, cur[begin])
        cur = get_deltas(cur)
    end

    push!(last_elements, 0)
    return last_elements
end

function main(filename::String)
    seqs = [
        [ parse(Int32, n) for n in split(strip(line), r"\s+") ]
        for line in readlines(filename)
    ]

    forecast = [
        foldr(-, steps_to_zeros(seq))
        for seq in seqs
    ]

    println(seqs)
    println(forecast)

    total = reduce(+, forecast)
    println("total: $total")
end

if length(ARGS) < 1
    println("usage: ", PROGRAM_FILE, " <input>")
else
    main(ARGS[1])
end