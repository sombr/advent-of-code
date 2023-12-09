using DataStructures

# this version uses time-pulling technique similar to DES simulations
# I admit, there's probably a quick mathematical way of solving these
# once you know all possible end-loops, their distances and move positions,
# but that way a bit too much and I settled for the DES approach.

function main(filename)
    lines = readlines(filename)

    moves = [ move == 'L' ? 1 : 2 for move in lines[1] ]
    edges::Vector{Tuple{String, String}} = [ Tuple(split(strip(edge), r"\s+=\s+"))  for edge in lines[3:length(lines)] ]

    edgemap::Dict{String, Tuple{String, String}} = Dict()
    for edge in edges
        edgemap[ edge[1] ] = Tuple( split(strip(edge[2])[begin+1:end-1], r"\s*,\s*") )
    end

    function find_path_from_node_and_step(start_node::String, start_step::Int64)::Tuple{String, Int64}
        node = start_node
        steps = 0

        visited::Set{Tuple{String, Int32}} = Set()

        while !endswith(node, 'Z') || steps == 0
            move_idx = ( (start_step+steps) % length(moves)) + 1
            if (node, move_idx) in visited
                return (node, -1)
            end

            push!(visited, (node, move_idx))
            move = moves[move_idx]

            new_node = edgemap[ node ][ move ]
            #println("move $node->$new_node with move $move")

            node = new_node
            steps += 1
        end

        return (node, steps)
    end


    start_nodes::Vector{String} = [ n for n in keys(edgemap) if endswith(n, 'A') ]

    # first, we'll have to reach end nodes everywhere, let's find those out
    start_to_z::Dict{String, Tuple{String, Int64}} = Dict([ node => find_path_from_node_and_step(node, 0) for node in start_nodes ])

    cache::Dict{Tuple{String, Int64}, Tuple{String, Int64}} = Dict()
    events = BinaryMinHeap([ (x[2], x[1]) for x in values(start_to_z)])
    steps::Int64 = 0
    progress::Int64 = 0
    while !isempty(events)
        reached = []
        while !isempty(events) && first(events)[1] == steps
            push!(reached, pop!(events))
        end

        if isempty(events)
            println("sym complete")
            break
        end

        # next cycle
        for (_, node) in reached
            move_idx = steps % length(moves)
            cache_key = (node, move_idx)
            if !haskey(cache, cache_key)
                cache[ cache_key ] = find_path_from_node_and_step(node, steps)
            end

            (next_node, dist) = cache[ cache_key ]
            push!(events, (steps + dist, next_node))
        end


        # get next time
        steps = first(events)[1]
        new_progress = steps ÷ 500_000_000
        if new_progress > progress
            println("cur steps $steps")
            progress = new_progress
        end
    end

    println(start_to_z)
    println(events)
    println(">>>> $steps")
    #println(moves, "\n", edges, "\n", edgemap, "\n")
end

if length(ARGS) < 1
    println("usage: ", PROGRAM_FILE, " <input>")
else
    main(ARGS[1])
end