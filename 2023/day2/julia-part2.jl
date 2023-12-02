function main(filename)
    total::Int32 = 0
    open(filename, "r") do io
        for line in eachline(io)
            prefix, rounds = split(line, ":")
            game_id = parse(UInt32, replace(prefix, ("Game" => ""), (" " => "")))

            rounds = [ strip(r) for r in split(rounds, ";") ]
            selections = [ split(strip(s), " ") for r in rounds for s in split(r, ",") ]
            counts = [ s[2] => parse(Int32, s[1]) for s in selections ]

            min_counts = Dict( "red" => 0, "green" => 0, "blue" => 0 )
            for count in counts
                if haskey(min_counts, count[1])
                    min_counts[count[1]] = max(min_counts[count[1]], count[2])
                end
            end

            power = 1
            for count in values(min_counts)
                power *= count
            end

            total += power
        end
    end

    println("result: ", total)
end

if length(ARGS) < 1
    println("usage: ", PROGRAM_FILE, " <input>")
else
    main(ARGS[1])
end