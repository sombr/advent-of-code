use std::fs;
use std::env;
use std::cmp::{min, max};

const NUMPAD: [[char; 5]; 5] = [
    ['0', '0', '1', '0', '0'],
    ['0', '2', '3', '4', '0'],
    ['5', '6', '7', '8', '9'],
    ['0', 'A', 'B', 'C', '0'],
    ['0', '0', 'D', '0', '0']
];

fn main() {
    let args: Vec<String> = env::args().collect();
    let content = fs::read_to_string(args[1].clone()).unwrap();
    let lines = content.split("\n").map(|s| s.to_owned()).collect::<Vec<String>>();

    let mut code: Vec<char> = Vec::new();
    let mut row: i8 = 2;
    let mut col: i8 = 0;

    let size: i8 = NUMPAD.len() as i8;

    for line in lines {
        if line.trim().len() == 0 {
            continue;
        }
        for m in line.chars() {
            match m {
                'U' => {
                    let nrow = max(0, row-1);
                    if NUMPAD[nrow as usize][col as usize] != '0' {
                        row = nrow;
                    }
                },
                'D' => {
                    let nrow = min(size-1, row+1);
                    if NUMPAD[nrow as usize][col as usize] != '0' {
                        row = nrow;
                    }
                },
                'R' => {
                    let ncol = min(size-1, col+1);
                    if NUMPAD[row as usize][ncol as usize] != '0' {
                        col = ncol;
                    }
                },
                'L' => {
                    let ncol = max(0, col-1);
                    if NUMPAD[row as usize][ncol as usize] != '0' {
                        col = ncol;
                    }
                },
                _ => println!("something else")
            }
        }
        code.push(NUMPAD[row as usize][col as usize]);
    }

    println!("part2 >>> {}", code.into_iter().collect::<String>());
}
