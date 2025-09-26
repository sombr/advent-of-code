import Foundation

func readInput(from filename: String) -> String {
    let content = try! String(contentsOfFile: filename, encoding: .utf8)
    return content
}

func prepareArray(_ string: String) -> Array<Character> {
    var arr: Array<Character> = Array()

    for sym in string {
        if sym.isNumber {
            arr.append(sym)
        }
    }

    return arr
}

func calculateMatchingSum(_ s: Array<Character>, with checkOffset: Int = 1) -> Int {
    var sum: Int = 0

    for (idx, sym) in s.enumerated() {
        let next_sym: Character = s[(idx+checkOffset) % s.count]
        if sym == next_sym {
            sum += sym.wholeNumberValue!
        }
    }

    return sum
}

func main() {
    let input = prepareArray(readInput(from: "input.txt"))
    var result = calculateMatchingSum(input)
    print("result part1: \(result)")

    result = calculateMatchingSum(input, with: input.count / 2)
    print("result part2: \(result)")
}

main()
