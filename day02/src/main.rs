use std::fs;

const MAX_DELTA: i32 = 3;

fn parse_input(input: &str) -> Vec<Vec<i32>> {
    input
        .lines()
        .map(|line| {
            line.split_whitespace()
                .map(|word| word.parse::<i32>().unwrap())
                .collect()
        })
        .collect()
}

fn is_consistently_increasing_or_decreasing(vec: &[i32], max_delta: i32) -> bool {
    if vec.len() < 2 {
        return true;
    }

    let mut is_still_increasing = true;
    let mut is_still_decreasing = true;

    for pair in vec.windows(2) {
        let delta = pair[1] - pair[0];
        if delta > 0 {
            is_still_decreasing = false;
        } else if delta < 0 {
            is_still_increasing = false;
        }
        if delta.abs() < 1 || delta.abs() > max_delta {
            return false;
        }
    }

    is_still_increasing || is_still_decreasing
}


fn solve_part1(data: Vec<Vec<i32>>) -> usize {
    data.iter()
        .filter(|vec| is_consistently_increasing_or_decreasing(vec.as_slice(), MAX_DELTA))
        .count()
}


/*fn solve_part2(data: &[i32]) -> i32 {
    *data.iter().max().unwrap()
}*/

fn main() {
    let input = fs::read_to_string("input.txt").expect("Failed to read input file");
    let data = parse_input(&input);

    let part1 = solve_part1(data);
    println!("Part 1: {}", part1);

    /*
    let part2 = solve_part2(&data);
    println!("Part 2: {}", part2);
    */
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_examples() {
        let example_input = r#"
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"#.trim_start();
        let data = parse_input(example_input);

        assert_eq!(solve_part1(data), 2);
        //assert_eq!(solve_part2(&data), 5);
    }
}
