use itertools::Itertools;
use std::fs;

#[derive(Debug)]
struct Operation {
    target_result: i64,   // Use i64 for larger values
    operations: Vec<i32>, // Keep i32 for smaller inputs
}

fn add(a: i64, b: i64) -> i64 {
    a + b
}

fn mul(a: i64, b: i64) -> i64 {
    a * b
}

fn concat(a: i64, b: i64) -> i64 {
    let b_len = (b as f64).log10().floor() as u32 + 1; // Number of digits in `b`
    a * 10_i64.pow(b_len) + b
}

const OPS: &[fn(i64, i64) -> i64] = &[add, mul];
const OPS2: &[fn(i64, i64) -> i64] = &[add, mul, concat];

fn parse_data(data: &str) -> Vec<Operation> {
    data.lines()
        .map(|row| {
            let mut parts = row.split(": ");
            let target_result = parts.next().unwrap().parse::<i64>().unwrap();
            let operations = parts
                .next()
                .unwrap()
                .split_whitespace()
                .map(|n| n.parse::<i32>().unwrap())
                .collect::<Vec<i32>>();

            Operation {
                target_result,
                operations,
            }
        })
        .collect()
}

fn solve_part1(input: &str, ops: &[fn(i64, i64) -> i64]) -> i64 {
    let data = parse_data(input);
    let mut total = 0;

    for operation in data {
        let mut found = false;

        // Generate operator combinations dynamically
        for combo in std::iter::repeat(ops)
            .take(operation.operations.len() - 1)
            .multi_cartesian_product()
        {
            if found {
                break; // Exit if a valid result has already been found
            }

            let mut result = operation.operations[0] as i64; // Promote to i64 for computation

            for (&num, op) in operation.operations[1..].iter().zip(combo.iter()) {
                result = op(result, num as i64); // Promote num to i64 for operations
                if result > operation.target_result {
                    break; // Prune invalid paths early
                }
            }

            if result == operation.target_result {
                total += result;
                found = true; // Stop evaluating more combinations
            }
        }
    }

    total
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
