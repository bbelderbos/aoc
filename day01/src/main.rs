use std::fs;
use std::collections::HashMap;

fn parse_input(input: &str) -> (Vec<i32>, Vec<i32>) {
    let mut col1 = Vec::new();
    let mut col2 = Vec::new();

    for line in input.lines() {
        let mut numbers = line.split_whitespace()
                              .map(|num| num.parse::<i32>().unwrap());
        col1.push(numbers.next().unwrap());
        col2.push(numbers.next().unwrap());
    }

    col1.sort();
    col2.sort();

    (col1, col2)
}

fn solve_part1(col1: &[i32], col2: &[i32]) -> i32 {
    col1.iter()
        .zip(col2.iter())
        .map(|(a, b)| (a - b).abs())
        .sum()
}

fn solve_part2(col1: &[i32], col2: &[i32]) -> i32 {
    let mut frequency_map = HashMap::new();
    for &num in col2 {
        *frequency_map.entry(num).or_insert(0) += 1;
    }

    col1.iter()
        .map(|&num| frequency_map.get(&num).unwrap_or(&0) * num)
        .sum()
}

fn main() {
    let input = fs::read_to_string("input.txt").expect("Failed to read input file");
    let (col1, col2) = parse_input(&input);
    let part1 = solve_part1(&col1, &col2);
    println!("Part 1: {}", part1);

    let part2 = solve_part2(&col1, &col2);
    println!("Part 2: {}", part2);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_examples() {
        let example_input = r#"
3   4
4   3
2   5
1   3
3   9
3   3
"#.trim_start();
        let (col1, col2) = parse_input(&example_input);
        assert_eq!(solve_part1(&col1, &col2), 11);
        assert_eq!(solve_part2(&col1, &col2), 31);
    }
}
