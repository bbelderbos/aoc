use std::fs;

fn string_to_matrix(input: &str) -> Vec<Vec<char>> {
    input.lines().map(|line| line.chars().collect()).collect()
}

fn extract_rows(matrix: &Vec<Vec<char>>) -> Vec<String> {
    matrix.iter().map(|row| row.iter().collect()).collect()
}

fn extract_columns(matrix: &Vec<Vec<char>>) -> Vec<String> {
    let cols = matrix[0].len();
    (0..cols)
        .map(|i| matrix.iter().map(|row| row[i]).collect())
        .collect()
}

fn extract_diagonals(matrix: &Vec<Vec<char>>) -> Vec<String> {
    let mut diagonals = Vec::new();
    let rows = matrix.len();
    let cols = matrix[0].len();

    for d in 0..(rows + cols - 1) {
        let mut diagonal = Vec::new();
        for r in (0.max(d as isize - cols as isize + 1) as usize)..(rows.min(d + 1)) {
            let c = d - r;
            diagonal.push(matrix[r][c]);
        }
        diagonals.push(diagonal.iter().collect());
    }

    for d in 0..(rows + cols - 1) {
        let mut diagonal = Vec::new();
        for r in (0.max(d as isize - cols as isize + 1) as usize)..(rows.min(d + 1)) {
            let c = cols - 1 - (d - r);
            diagonal.push(matrix[r][c]);
        }
        diagonals.push(diagonal.iter().collect());
    }

    diagonals
}

fn count_occurrences(string: &str) -> usize {
    let search_string = "XMAS";
    let rev_search_string: String = search_string.chars().rev().collect();

    let n = search_string.len();
    if string.len() < n {
        return 0;
    }

    let mut count = 0;
    for i in 0..=(string.len() - n) {
        let segment: String = string.chars().skip(i).take(n).collect();
        if segment == search_string || segment == rev_search_string {
            count += 1;
        }
    }
    count
}

fn solve_part1(input: &str) -> usize {
    let matrix = string_to_matrix(&input.trim());

    let rows = extract_rows(&matrix);
    let columns = extract_columns(&matrix);
    let diagonals = extract_diagonals(&matrix);

    let mut results = 0;

    for row in &rows {
        results += count_occurrences(row);
    }

    for column in &columns {
        results += count_occurrences(column);
    }

    for diagonal in &diagonals {
        results += count_occurrences(diagonal);
    }

    results
}

// fn solve_part2(data: &[i32]) -> i32 {
//    todo!();
// }

fn main() {
    let input = fs::read_to_string("input.txt").expect("Failed to read input file");

    let part1 = solve_part1(&input);
    println!("Part 1: {}", part1);

    // let part2 = solve_part2(&input);
    // println!("Part 2: {}", part2);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_examples() {
        let input = r#"
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"#
        .trim();
        let file_input = fs::read_to_string("input.txt").expect("Failed to read input file");
        assert_eq!(solve_part1(&input), 18);
        assert_eq!(solve_part1(&file_input), 2633);
        // assert_eq!(solve_part2(&input), 1);
        // assert_eq!(solve_part2(&file_input), 1);
    }
}
