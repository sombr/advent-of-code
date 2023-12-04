

function main(filename)
    wins = []
    counts = []
    open(filename, "r") do io
        for line in eachline(io)
            card, data = split(line, ":")
            win, have = split(data, "|")

            winset = Set([ strip(x) for x in split(strip(win), " ") if strip(x) != "" ])
            winhave = Set([ strip(x) for x in split(strip(have), " ") if strip(x) in winset ])

            push!(wins, length(winhave))
            push!(counts, 1)
        end
    end

    for (idx, win) in enumerate(wins)
        for offset in 1:win
            counts[ idx + offset ] += counts[idx]
        end
    end

    total = reduce(+, counts)

    println("result: ", total)
end

if length(ARGS) < 1
    println("usage: ", PROGRAM_FILE, " <input>")
else
    main(ARGS[1])
end