use std::fs;
use regex::Regex;

fn extract_group(caps: &regex::Captures, idx: usize) -> Option<i32> {
    caps.get(idx)?.as_str().parse::<i32>().ok()
}

fn parse_input(input: &str) -> Vec<(i32, i32)> {
    let pattern = r"mul\((\d+),(\d+)\)";
    let re = Regex::new(pattern).unwrap();
    let matches: Vec<(i32, i32)> = re
        .captures_iter(input)
        .filter_map(|caps| {
            Some((
                extract_group(&caps, 1)?,
                extract_group(&caps, 2)?,
            ))
        })
        .collect();
    matches
}

fn solve_part1(data: &[(i32, i32)]) -> i32 {
    let mut result = 0;
    for (group1, group2) in data {
        result += group1 * group2;
    }
    result
}

// fn solve_part2(data: &[i32]) -> i32 {
//    todo!();
// }

fn main() {
    let input = fs::read_to_string("input.txt").expect("Failed to read input file");
    let data = parse_input(&input);

    let part1 = solve_part1(&data);
    println!("Part 1: {}", part1);

    // let part2 = solve_part2(&data);
    // println!("Part 2: {}", part2);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_examples() {
        let example_input = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))";
        let data = parse_input(example_input);

        assert_eq!(solve_part1(&data), 161);
        // assert_eq!(solve_part2(&data), 5);
    }
}
