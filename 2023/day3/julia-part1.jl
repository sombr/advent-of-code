
function get_valid_adjacency(r, c, rows, cols, row_steps, col_steps)
    res = []
    for rd in row_steps
        for cd in col_steps
            if rd == 0 && cd == 0
                continue
            end

            rc = r + rd
            cc = c + cd
            
            if rc < 1 || rc > rows
                continue
            end
            if cc < 1 || cc > cols
                continue
            end

            push!(res, (rc,cc))
        end
    end

    return res
end

function get_valid_numbers(lines::Vector{String})
    rows::Integer = length(lines)
    cols::Integer = length(lines[1])

    valid_numbers = Matrix{Char}(undef, rows, cols)
    fill!(valid_numbers, ' ')
    visited = zeros(Int8, (rows, cols))

    for r in 1:rows
        for c in 1:cols
            symbol::Char = lines[r][c]

            # skip empty
            if symbol == '.'
                continue
            end

            if visited[ r, c ] > 0
                continue
            end

            # found a symbol, look for numbers around
            if !isdigit(symbol)
                queue = get_valid_adjacency(r,c, rows, cols, [-1,0,1], [-1,0,1])

                while !isempty(queue)
                    cur = pop!(queue)
                    candidate = lines[cur[1]][cur[2]]

                    if isdigit(candidate)
                        visited[ cur[1], cur[2] ] = 1
                        valid_numbers[cur[1], cur[2]] = candidate

                        digit_adj = get_valid_adjacency( cur[1], cur[2], rows, cols, [0], [-1, 1])
                        for da in digit_adj
                            if visited[ da[1], da[2] ] < 1
                                push!(queue, da)
                            end
                        end
                    end
                end
            end
        end
    end

    return valid_numbers
end

function main(filename)
    lines::Vector{String} = []

    open(filename, "r") do io
        lines = readlines(io)
    end

    rows::Integer = length(lines)
    cols::Integer = length(lines[1])

    valid_numbers = get_valid_numbers(lines)

    total = 0
    for r in 1:rows
        for num in [ n for n in split(join(valid_numbers[r, :], ""), " ") if length(n) > 0 ]
            total += parse(Int32, num)
        end
    end

    println("result: ", total)
end

if length(ARGS) < 1
    println("usage: ", PROGRAM_FILE, " <input>")
else
    @time main(ARGS[1])
end