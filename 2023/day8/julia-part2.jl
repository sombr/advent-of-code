# this is a super-slow brute force version which I haven't seen ever complete
# see the DES version for a faster (albeit still somewhat slow) version that 
# actually does complete.

function main(filename)
    lines = readlines(filename)

    moves = [ move == 'L' ? 1 : 2 for move in lines[1] ]
    edges::Vector{Tuple{String, String}} = [ Tuple(split(strip(edge), r"\s+=\s+"))  for edge in lines[3:length(lines)] ]

    edgemap::Dict{String, Tuple{String, String}} = Dict()
    for edge in edges
        edgemap[ edge[1] ] = Tuple( split(strip(edge[2])[begin+1:end-1], r"\s*,\s*") )
    end

    nodes::Vector{String} = [ n for n in keys(edgemap) if endswith(n, 'A') ]
    steps::UInt64 = 0
    atZ = 0
    while atZ != length(nodes)
        for nidx in eachindex(nodes)
            move_idx = ( steps % length(moves) ) + 1
            move = moves[ move_idx ]

            cur_node = nodes[nidx]
            new_node = edgemap[ cur_node ][move]
            
            nodes[nidx] = new_node

            delta = endswith(new_node, 'Z') - endswith(cur_node, 'Z')
            atZ += delta
        end
        steps += 1
        if steps % 5_000_000 == 0
            println(">> steps $steps")
        end
    end

    println(moves, "\n", edges, "\n", edgemap, "\n", steps)
end

if length(ARGS) < 1
    println("usage: ", PROGRAM_FILE, " <input>")
else
    main(ARGS[1])
end