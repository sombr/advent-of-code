TOTAL = Dict(
    "red" => 12,
    "green" => 13,
    "blue" => 14
)

function main(filename)
    total::Int32 = 0
    open(filename, "r") do io
        for line in eachline(io)
            prefix, rounds = split(line, ":")
            game_id = parse(UInt32, replace(prefix, ("Game" => ""), (" " => "")))

            rounds = [ strip(r) for r in split(rounds, ";") ]
            selections = [ split(strip(s), " ") for r in rounds for s in split(r, ",") ]
            counts = [ s[2] => parse(Int32, s[1]) for s in selections ]

            is_possible = true
            for count in counts
                if !(count[1] in keys(TOTAL)) || (count[2] > TOTAL[ count[1] ])
                    is_possible = false
                    break
                end
            end

            if is_possible
                total += game_id
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