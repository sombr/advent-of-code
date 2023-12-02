
function find_first_digit(line::String)::Int8
    for sym in line
        if isdigit(sym)
            return parse(Int8, sym)
        end
    end
end

function main(filename::String)
    total::Int32 = 0
    open(filename, "r") do file
        for line in eachline(file)
            invline = reverse(line)

            number = find_first_digit(line) * 10 + find_first_digit(invline)
            total += number
        end
    end

    println("result: ", total)
end

if length(ARGS) < 1
    println("usage: ", PROGRAM_FILE, " <file>")
else
    main(ARGS[1])
end