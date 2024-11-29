use std::fs;
use std::env;
use std::cmp::{min, max};

const NUMPAD: [[u8; 3]; 3] = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];

fn main() {
    let args: Vec<String> = env::args().collect();
    let content = fs::read_to_string(args[1].clone()).unwrap();
    let lines = content.split("\n").map(|s| s.to_owned()).collect::<Vec<String>>();

    let mut code: Vec<u8> = Vec::new();
    let mut row: i8 = 0;
    let mut col: i8 = 0;

    let size: i8 = NUMPAD.len() as i8;

    for line in lines {
        if line.trim().len() == 0 {
            continue;
        }
        for m in line.chars() {
            match m {
                'U' => row = max(0, row-1),
                'D' => row = min(size-1, row+1),
                'R' => col = min(size-1, col+1),
                'L' => col = max(0, col-1),
                _ => println!("something else")
            }
        }
        code.push(NUMPAD[row as usize][col as usize]);
    }

    let strcode: Vec<String> = code.into_iter().map(|x| format!("{}", x) ).collect();
    println!("part1 >>> {}", strcode.join(""));
}
