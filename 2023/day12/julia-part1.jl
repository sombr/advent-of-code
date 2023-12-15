mutable struct Wrapper
    acc::Int32
    level::Int32
end

function valid_solution(pos, blocks)
    return isempty(pos) && ( isempty(blocks) || (length(blocks) == 1 && blocks[begin] == 0) )
end

function valid_choice(choice, blocks, solution)
    read_sym = choice == '#' && length(blocks) > 0 && blocks[begin] > 0
    non_block = isempty(solution) || solution[end] == '.'
    end_block = length(blocks) > 0 && blocks[begin] == 0
    read_empty = choice == '.' && ( non_block || end_block )

    return read_sym || read_empty
end

function backtrack_read(positions, blocks, res::Wrapper, solution::Vector{Char}, debug = false)
    if valid_solution(positions, blocks)
        res.acc += 1
        if debug
            println(res.level, " valid solution: ", String(solution), " $positions | $blocks | $res")
        end
    else # continue
        # no choice
        choice_to_read = isempty(positions) ? [] : positions[begin] == '?' ? ['.', '#'] : [positions[begin]]

        # choice
        for choice in choice_to_read
            positions[begin] = choice

            if debug
                println(res.level, " trying: $choice -- ",  String(solution), "|", String(positions), " with choices:$choice_to_read blocks: $blocks")
            end
            if !valid_choice(choice, blocks, solution)
                continue
            end

            # apply choice
            new_blocks = copy(blocks)
            if choice == '#'
                new_blocks[begin] -= 1
            elseif length(new_blocks) > 0 && new_blocks[begin] == 0
                new_blocks = new_blocks[begin+1:end]
            end

            push!(solution, choice)
            res.level += 1
            backtrack_read(positions[begin+1:end], new_blocks, res, solution, debug)
            res.level -= 1
            pop!(solution)
        end
    end
end

function main(filename)
    lines = readlines(filename)

    total = 0
    for line in lines
        positions, counts = split(line, r"\s+")
        counts = [ parse(Int32, n) for n in split(counts, ",")]
        positions = [ ch for ch in positions ]

        acc::Wrapper = Wrapper(0, 0)
        sol::Vector{Char} = []
        println("--- reading ", String(positions), " --- $counts")
        backtrack_read(positions, counts, acc, sol, false)

        res = acc.acc

        println("--- res: $res ")

        total += res
    end

    println("total: $total")
end

if length(ARGS) < 1
    println("usage: ", PROGRAM_FILE, " <input>")
else
    main(ARGS[1])
end