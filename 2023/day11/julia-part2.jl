
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

function get_dist(a, b, er, ec)
    row_step = sign(b[1] - a[1])
    if row_step == 0
        row_step = 1
    end

    col_step = sign(b[2] - a[2])
    if col_step == 0
        col_step = 1
    end

    all_rows = a[1]:row_step:b[1]
    all_cols = a[2]:col_step:b[2]

    empty_rows = [ r for r in all_rows if r in er ]
    empty_cols = [ c for c in all_cols if c in ec ]

    standard_dist = length(all_rows) - length(empty_rows) + length(all_cols) - length(empty_cols) - 2
    expanded_dist = length(empty_rows) * 1000000 + length(empty_cols) * 1000000

    return standard_dist + expanded_dist
end

function main(filename)
    rows = readlines(filename)

    er, ec = find_empty_rows_and_cols(rows)
    println("empty rows: $er, cols: $ec")
    galaxies = find_all_galaxies(rows)

    perms = get_permuations(galaxies)

    res = reduce(+, [ get_dist(p..., er, ec) for p in perms ])
    println("res: $res")
end


if length(ARGS) < 1
    println("usage: ", PROGRAM_FILE, " <input>")
else
    main(ARGS[1])
end