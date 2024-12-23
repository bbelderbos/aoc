use regex::Regex;
use std::fs;

fn _extract_group(caps: &regex::Captures, idx: usize) -> Option<i32> {
    caps.get(idx)?.as_str().parse::<i32>().ok()
}

fn extract_multiplication_pairs(input: &str) -> Vec<(i32, i32)> {
    let pattern = r"mul\((\d+),(\d+)\)";
    let re = Regex::new(pattern).unwrap();
    let matches: Vec<(i32, i32)> = re
        .captures_iter(input)
        .filter_map(|caps| Some((_extract_group(&caps, 1)?, _extract_group(&caps, 2)?)))
        .collect();
    matches
}

fn parse_enabled_chunks(input: &str) -> Vec<String> {
    let chunks: Vec<String> = input.split("do()").map(|x| x.to_string()).collect();
    let mut results = Vec::new();

    for chunk in chunks {
        if chunk.contains("don't()") {
            results.push(chunk.split("don't()").next().unwrap().trim().to_string());
        } else {
            results.push(chunk.trim().to_string());
        }
    }
    results
}

fn solve_part1(input: &str) -> i32 {
    let data = extract_multiplication_pairs(input);
    let mut result = 0;
    for (group1, group2) in data {
        result += group1 * group2;
    }
    result
}

fn solve_part2(input: &str) -> i32 {
    let chunks = parse_enabled_chunks(input);
    let mut result = 0;
    for chunk in chunks {
        let data = extract_multiplication_pairs(&chunk);
        for (group1, group2) in data {
            result += group1 * group2;
        }
    }
    result
}

fn main() {
    let input = fs::read_to_string("input.txt").expect("Failed to read input file");

    let part1 = solve_part1(&input);
    println!("Part 1: {}", part1);

    let part2 = solve_part2(&input);
    println!("Part 2: {}", part2);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_examples() {
        let mut input = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))";
        let file_input = fs::read_to_string("input.txt").expect("Failed to read input file");

        assert_eq!(solve_part1(&input), 161);
        assert_eq!(solve_part1(&file_input), 157621318);

        input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))";
        assert_eq!(solve_part2(&input), 48);
        assert_eq!(solve_part2(&file_input), 79845780);
    }
}
