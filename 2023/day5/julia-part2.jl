function read_input(filename)
    seeds = []
    type_map = Dict{String, String}()
    data_map = Dict{String, Vector{Tuple{Int64, Int64, Int64}}}()

    open(filename, "r") do io
        map_from = ""
        map_to = ""
        for line in eachline(io)

            if startswith(line, "seeds:")
                seeds = [ parse(Int64, x) for x in split(strip(split(line, ":")[2]), r"\s+") ]

                odd_start = [ x for (idx, x) in enumerate(seeds) if idx % 2 != 0 ]
                even_len = [ x for (idx, x) in enumerate(seeds) if idx % 2 == 0 ]

                seeds = [ p for p in zip(odd_start, even_len) ]

                continue
            end

            if endswith(line, "map:")
                map_from, map_to = split(strip(split(line, r"\s+")[1]), "-to-")
                type_map[map_from] = map_to
                data_map[map_from] = []
                continue
            end

            if strip(line) == ""
                map_from = ""
                map_to = ""
                continue
            end

            # read ranges
            range_to, range_from, range_len = [ parse(Int64, x) for x in split(strip(line), r"\s+") ]
            push!(data_map[map_from], (range_from, range_to, range_len))
        end
    end

    return (seeds, type_map, data_map)
end

function map_with_sorted_ranges(value::Int64, ranges::Vector{Tuple{Int64, Int64, Int64}})::Int64
    ins_index = searchsortedfirst(ranges, value, by=x->x[1], lt=(a,b)->a<=b)

    # not in any range
    if ins_index == 1
        return value
    end

    check_range = ranges[ ins_index - 1 ]

    # out of the best matched range
    if value >= check_range[1] + check_range[3]
        return value
    end

    res = (value - check_range[1]) + check_range[2]
    return res
end

function main(filename)
    seeds, typemap, datamap = read_input(filename)
    println(">>> seeds ", seeds)
    println(">>> types ", typemap)
    println(">>> data ", datamap)

    for key in keys(datamap)
        sort!(datamap[key])
    end

    min_loc = nothing
    for seed_range in seeds
        for seed in seed_range[1]:(seed_range[1]+seed_range[2]-1)
            start_type = "seed"
            start_value = seed

            for _ in 1:7
                next_type = typemap[start_type]
                start_value = map_with_sorted_ranges(start_value, datamap[start_type])
                start_type = next_type
            end

            if isnothing(min_loc) || min_loc > start_value
                min_loc = start_value
            end
        end
    end

    println("min loc: ", min_loc)
end

if length(ARGS) < 1
    print("usage: ", PROGRAM_FILE, " < input >")
else
    @time main(ARGS[1])
end