#!/usr/bin/env julia

const XMAS::String = "XMAS"

function can_read_xmas(field::Vector{String}, start_row::Int, start_col::Int, dr::Int, dc::Int)::Bool
    rows::Int = length(field)
    cols::Int = rows > 0 ? length(field[1]) : 0

    for offset in range(0, length(XMAS)-1)
        r = start_row + dr * offset
        c = start_col + dc * offset

        if r < 1 || r > rows || c < 1 || c > cols
            return false
        end

        if field[r][c] != XMAS[offset+1]
            return false
        end
    end

    return true
end

function main(filename::String)
    field = readlines(filename)

    rows::Int = length(field)
    cols::Int = rows > 0 ? length(field[1]) : 0

    xmas_count::Int = 0
    for row in range(1, rows)
        for col in range(1, cols)
            for dr in (-1,0,1)
                for dc in (-1,0,1)
                    if dr == 0 && dc == 0
                        continue
                    end

                    if can_read_xmas(field, row, col, dr, dc)
                        xmas_count += 1
                    end
                end
            end
        end
    end

    println("part1 >> $xmas_count")
end

main(ARGS[1])
