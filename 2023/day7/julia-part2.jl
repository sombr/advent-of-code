CARD_VALUE::Dict{Char, Int8} = Dict(
    [ x[1] => idx for (idx, x) in enumerate(reverse(
        # J is the worst now
        split("A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J", ", ")
    )) ]
)

function get_hand_value(hand::Vector{Char})::Tuple{Int8, String}
    per_card_val::String = ""
    card_counts::Dict{Char, Int8} = Dict()

    max_count::Int8 = 0
    for card in hand
        per_card_val *= 'a' + CARD_VALUE[card]
        card_counts[card] = get(card_counts, card, 0) + 1
        max_count = max(max_count, card_counts[card])
    end

    hand_rank = 0

    card_cats::Int8 = length(card_counts)
    # five of a kind [AAAAA]
    if card_cats == 1
        hand_rank = 7
        # if [JJJJJ] -- no change
    # four of a kind [AAAA|B]
    elseif card_cats == 2 && max_count == 4
        hand_rank = 6
        # if [JJJJ|A] or [AAAA|J] -- we can only merge and go up
        if get(card_counts, 'J', 0) > 0
            hand_rank = 7
        end
    # full house [AAA|BB]
    elseif card_cats == 2 && max_count == 3
        hand_rank = 5
        # if [JJJ|AA] or [AAA|JJ] -- we can only merge and go up top
        if get(card_counts, 'J', 0) > 0
            hand_rank = 7
        end
    # three of a kind [AAA|B|C]
    elseif card_cats == 3 && max_count == 3
        hand_rank = 4
        # if [AAA|B|J] or [AAA|J|C] or [JJJ|B|C] -- the best is to merge into 4 of kind
        if get(card_counts, 'J', 0) > 0
            hand_rank = 6
        end
    # two pairs [AA|BB|C]
    elseif card_cats == 3 && max_count == 2
        hand_rank = 3
        # if [AA|BB|J] -- best is to merge into full house
        # if [AA|JJ|C] or [JJ|BB|C] -- the best is to merge into 4 kind
        if get(card_counts, 'J', 0) > 0
            hand_rank = 5
        end
        if get(card_counts, 'J', 0) > 1
            hand_rank = 6
        end
    # one pair [AA|B|C|D]
    elseif card_cats == 4 && max_count == 2
        hand_rank = 2
        # if [JJ|B|C|D] or [AA|J|C|D] -- best is 3 of kind
        if get(card_counts, 'J', 0) > 0
            hand_rank = 4
        end
    # high card [A|B|C|D|E]
    elseif card_cats == 5
        hand_rank = 1
        # if [J|B|C|D|E] -- best is 1 pair
        if get(card_counts, 'J', 0) > 0
            hand_rank = 2
        end
    else
        println("unknown hand cat: $hand")
    end

    return (hand_rank, per_card_val)
end

function main(filename)
    hands::Dict{Tuple{Int8, String}, Vector{Int32}} = Dict()

    open(filename, "r") do io
        for line in eachline(io)
            hand, bid = split(line, r"\s+")
            
            hand = [ x for x in hand ]
            bid = parse(Int32, bid)

            hand_value = get_hand_value(hand)

            hands[hand_value] = get(hands, hand_value, [] )
            push!(hands[hand_value] , bid)
        end
    end

    ordered_hands = [ x for x in keys(hands) ]
    sort!(ordered_hands)

    total::Int32 = 0
    for (rank, hand) in enumerate(ordered_hands)
        total += reduce(+, map( x -> x * rank, hands[hand] ))
    end

    println(hands)

    println("total: ", total)
end

if length(ARGS) < 1
    print("use: ", PROGRAM_FILE, " <input>")
else
    main(ARGS[1])
end