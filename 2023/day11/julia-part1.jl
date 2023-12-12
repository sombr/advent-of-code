
function find_empty_rows_and_cols(space)
    rows = Set([ x for x in eachindex(space) ])
    cols = Set([ x for x in eachindex(space[begin]) ])

    for r in eachindex(space)
        for c in eachindex(space[r])
            sym = space[r][c]
            if sym == '#'
                delete!(rows, r)
                delete!(cols, c)
            end
        end
    end

    return (rows, cols)
end

function expand_universe(space, empty_rows, empty_cols)
    universe = []
    for r in eachindex(space)
        row = []
        for c in eachindex(space[r])
            sym = space[r][c]
            push!(row, sym)
            if c in empty_cols
                push!(row, sym)
            end
        end
        push!(universe, row)
        if r in empty_rows
            push!(universe, [ x for x in row ])
        end
    end

    return universe
end

function find_all_galaxies(space)
    res = []
    for r in eachindex(space)
        for c in eachindex(space[r])
            sym = space[r][c]
            if sym == '#'
                push!(res, (r,c))
            end
        end
    end

    return res
end

function get_permuations(xs)
    res = []
    for x in eachindex(xs)
        for y in (x+1):length(xs)
            push!(res, (xs[x], xs[y]))
        end
    end

    return res
end

function get_dist(a, b)
    return abs(a[1] - b[1]) + abs(a[2] - b[2])
end

function main(filename)
    rows = readlines(filename)

    er, ec = find_empty_rows_and_cols(rows)
    println("empty rows: $er, cols: $ec")
    println("original size: ", length(rows), " x ", length(rows[1]))
    uni = expand_universe(rows, er, ec)
    println("new size: ", length(uni), " x ", length(uni[1]))

    galaxies = find_all_galaxies(uni)

    perms = get_permuations(galaxies)

    res = reduce(+, [ get_dist(p...) for p in perms ])
    println("res: $res")
end


if length(ARGS) < 1
    println("usage: ", PROGRAM_FILE, " <input>")
else
    main(ARGS[1])
end