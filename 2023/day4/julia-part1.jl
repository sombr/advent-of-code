

function main(filename)
    total = 0
    open(filename, "r") do io
        for line in eachline(io)
            card, data = split(line, ":")
            win, have = split(data, "|")

            winset = Set([ strip(x) for x in split(strip(win), " ") if strip(x) != "" ])
            winhave = Set([ strip(x) for x in split(strip(have), " ") if strip(x) in winset ])

            if length(winhave) > 0
                value = 2 ^ ( length(winhave) - 1 )
                total += value
            end
        end
    end

    println("result: ", total)
end

if length(ARGS) < 1
    println("usage: ", PROGRAM_FILE, " <input>")
else
    main(ARGS[1])
end