WORDS::Vector{String} = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
REV_WORDS = [ reverse(w) for w in WORDS ]

function find_first_digit(line::String, words::Vector{String})::Int8
    min_pos::Int32 = length(line)
    digit = -1

    for (idx, sym) in enumerate(line)
        if isdigit(sym)
            digit = parse(Int8, sym)
            min_pos = idx
            break
        end
    end

    for (idx, word) in enumerate(words)
        pos = findfirst(word, line)
        if !isnothing(pos)
            pos = first(pos)
            if pos < min_pos
                digit = idx
                min_pos = pos
            end
        end
    end

    return digit
end

function main(filename::String)
    total::Int32 = 0
    open(filename, "r") do file
        for line in eachline(file)
            invline = reverse(line)

            number = find_first_digit(line, WORDS) * 10 + find_first_digit(invline, REV_WORDS)
            total += number
        end
    end

    println("result: ", total)
end

if length(ARGS) < 1
    println("usage: ", PROGRAM_FILE, " <file>")
else
    @time main(ARGS[1])
end