use itertools::Itertools;
use std::fs;

#[derive(Debug)]
struct Operation {
    target_result: i64,
    operations: Vec<i64>,
}

fn add(a: i64, b: i64) -> i64 {
    a + b
}

fn mul(a: i64, b: i64) -> i64 {
    a * b
}

fn concat(a: i64, b: i64) -> i64 {
    let mut concatenated = a.to_string();
    concatenated.push_str(&b.to_string());
    concatenated.parse::<i64>().unwrap()
}

const OPS: &[fn(i64, i64) -> i64] = &[add, mul];
const OPS2: &[fn(i64, i64) -> i64] = &[add, mul, concat];

fn parse_data(data: &str) -> impl Iterator<Item = Operation> + '_ {
    data.lines().map(|row| {
        let mut parts = row.split(": ");
        let target_result = parts.next().unwrap().parse::<i64>().unwrap();
        let operations = parts
            .next()
            .unwrap()
            .split_whitespace()
            .map(|n| n.parse::<i64>().unwrap())
            .collect::<Vec<i64>>();

        Operation {
            target_result,
            operations,
        }
    })
}

fn solve_part1(input: &str, ops: &[fn(i64, i64) -> i64]) -> i64 {
    let data = parse_data(input);
    let mut valid: Vec<i64> = Vec::new();

    for operation in data {
        let mut found = false;

        // Convert `ops` to owned items for multi_cartesian_product
        for combo in vec![ops.to_vec(); operation.operations.len() - 1]
            .into_iter()
            .multi_cartesian_product()
        {
            if found {
                break; // Exit if a valid result has already been found
            }

            let mut result = operation.operations[0];
            let mut is_valid = true;

            for (&num, op) in operation.operations[1..].iter().zip(combo.iter()) {
                result = op(result, num);
                if result > operation.target_result {
                    is_valid = false; // Prune invalid paths
                    break;
                }
            }

            if is_valid && result == operation.target_result {
                valid.push(result);
                found = true; // Stop evaluating more combinations
            }
        }
    }

    valid.iter().sum()
}

fn solve_part2(input: &str, ops2: &[fn(i64, i64) -> i64]) -> i64 {
    solve_part1(input, ops2)
}

fn main() {
    let input = fs::read_to_string("input.txt").expect("Failed to read input file");

    let part1 = solve_part1(&input, OPS);
    println!("Part 1: {}", part1);

    let part2 = solve_part2(&input, OPS2);
    println!("Part 2: {}", part2);
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    fn get_input() -> &'static str {
        r#"
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"#
        .trim()
    }

    fn get_file_input() -> String {
        fs::read_to_string("input.txt").expect("Failed to read input file")
    }

    #[test]
    fn test_part1() {
        let input = get_input();
        let file_input = get_file_input();
        assert_eq!(solve_part1(input, OPS), 3749);
        assert_eq!(solve_part1(&file_input, OPS), 5837374519342);
    }

    #[test]
    fn test_part2() {
        let input = get_input();
        let file_input = get_file_input();
        assert_eq!(solve_part2(input, OPS2), 11387);
        assert_eq!(solve_part2(&file_input, OPS2), 492383931650959);
    }
}
