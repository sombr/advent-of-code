
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
    visited = [ [ Set{Int32}() for c in 1:cols ] for r in 1:rows  ]

    star_count = 0

    for r in 1:rows
        for c in 1:cols
            symbol::Char = lines[r][c]

            # skip empty
            if symbol == '.'
                continue
            end

            # found a symbol, look for numbers around
            if symbol == '*'
                star_count += 1
                queue = get_valid_adjacency(r,c, rows, cols, [-1,0,1], [-1,0,1])

                while !isempty(queue)
                    cur = pop!(queue)
                    candidate = lines[cur[1]][cur[2]]

                    if isdigit(candidate)
                        push!( visited[ cur[1] ][ cur[2] ], star_count )
                        valid_numbers[cur[1], cur[2]] = candidate

                        digit_adj = get_valid_adjacency( cur[1], cur[2], rows, cols, [0], [-1, 1])
                        for da in digit_adj
                            if !( star_count in visited[ da[1] ][ da[2] ] )
                                push!(queue, da)
                            end
                        end
                    end
                end
            end
        end
    end

    return valid_numbers, visited
end

function add_number_with_reach!(acc, number, reach)
    if number != ""
        for star_idx in reach
            if !haskey(acc, star_idx)
                acc[star_idx] = []
            end
            push!(acc[star_idx], parse(Int32, number))
        end
    end
end

function main(filename)
    lines::Vector{String} = []

    open(filename, "r") do io
        lines = readlines(io)
    end

    rows::Integer = length(lines)
    cols::Integer = length(lines[1])

    valid_numbers, star_visits = get_valid_numbers(lines)

    star_numbers = Dict{Int32, Vector{Int32}}()
    for r in 1:rows
        cur_num = ""
        cur_reach = Set()
        for c in 1:cols
            if isdigit( valid_numbers[r, c] )
                cur_num *= valid_numbers[r,c]
                cur_reach = star_visits[r][c]
            else
                add_number_with_reach!(star_numbers, cur_num, cur_reach)
                cur_num = ""
                cur_reach = Set()
            end
        end
        add_number_with_reach!(star_numbers, cur_num, cur_reach)
    end

    total = 0
    for nums in values(star_numbers)
        if length(nums) == 2
            total += reduce(*, nums)
        end
    end

    show(stdout, "text/plain", star_numbers)
    println("")
    println("result: ", total)
end

if length(ARGS) < 1
    println("usage: ", PROGRAM_FILE, " <input>")
else
    @time main(ARGS[1])
end
