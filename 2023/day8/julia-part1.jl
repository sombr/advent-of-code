

function main(filename)
    lines = readlines(filename)

    moves = [ move == 'L' ? 1 : 2 for move in lines[1] ]
    edges::Vector{Tuple{String, String}} = [ Tuple(split(strip(edge), r"\s+=\s+"))  for edge in lines[3:length(lines)] ]

    edgemap::Dict{String, Tuple{String, String}} = Dict()
    for edge in edges
        edgemap[ edge[1] ] = Tuple( split(strip(edge[2])[begin+1:end-1], r"\s*,\s*") )
    end

    node = "AAA"
    steps = 0
    while node != "ZZZ"
        move_idx = ( steps % length(moves) ) + 1
        move = moves[ move_idx ]

        steps += 1
        node = edgemap[ node ][move]
    end

    println(moves, "\n", edges, "\n", edgemap, "\n", steps)
end

if length(ARGS) < 1
    println("usage: ", PROGRAM_FILE, " <input>")
else
    main(ARGS[1])
end