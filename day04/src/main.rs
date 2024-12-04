use std::fs;

const SEARCH_STRING: &str = "XMAS";
const REVERSE_SEARCH_STRING: &str = "SAMX";

fn string_to_matrix(input: &str) -> Vec<Vec<char>> {
    input.lines().map(|line| line.chars().collect()).collect()
}

fn validate_matrix(matrix: &Vec<Vec<char>>) -> Result<(), String> {
    let row_len = matrix[0].len();
    if matrix.iter().any(|row| row.len() != row_len) {
        Err("Matrix rows have inconsistent lengths".to_string())
    } else {
        Ok(())
    }
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
    let n = SEARCH_STRING.len();
    if string.len() < n {
        return 0;
    }

    let mut count = 0;
    for i in 0..=(string.len() - n) {
        if &string[i..i + n] == SEARCH_STRING || &string[i..i + n] == REVERSE_SEARCH_STRING {
            count += 1;
        }
    }

    count
}

fn solve_part1(input: &str) -> usize {
    let matrix = string_to_matrix(&input.trim());

    if let Err(err) = validate_matrix(&matrix) {
        panic!("Invalid matrix: {}", err);
    }

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

fn get_submatrices(
    matrix: &Vec<Vec<char>>,
    sub_rows: usize,
    sub_cols: usize,
) -> Vec<Vec<Vec<char>>> {
    let rows = matrix.len();
    let cols = matrix[0].len();
    let mut submatrices = Vec::new();

    for i in 0..=(rows - sub_rows) {
        for j in 0..=(cols - sub_cols) {
            let submatrix: Vec<Vec<char>> = (i..i + sub_rows)
                .map(|x| matrix[x][j..j + sub_cols].to_vec())
                .collect();
            submatrices.push(submatrix);
        }
    }

    submatrices
}

fn match_submatrix(submatrix: &Vec<Vec<char>>) -> bool {
    if submatrix[1][1] != 'A' {
        return false;
    }

    // check valid Xs
    if submatrix[0][0] == 'M'
        && submatrix[2][2] == 'S'
        && submatrix[0][2] == 'S'
        && submatrix[2][0] == 'M'
    {
        return true;
    }
    if submatrix[0][0] == 'S'
        && submatrix[2][2] == 'M'
        && submatrix[0][2] == 'M'
        && submatrix[2][0] == 'S'
    {
        return true;
    }
    if submatrix[2][0] == 'M'
        && submatrix[0][2] == 'S'
        && submatrix[0][0] == 'S'
        && submatrix[2][2] == 'M'
    {
        return true;
    }
    if submatrix[2][0] == 'S'
        && submatrix[0][2] == 'M'
        && submatrix[0][0] == 'M'
        && submatrix[2][2] == 'S'
    {
        return true;
    }

    false
}

fn solve_part2(input: &str) -> usize {
    let matrix = string_to_matrix(&input.trim());

    if let Err(err) = validate_matrix(&matrix) {
        panic!("Invalid matrix: {}", err);
    }

    let submatrices = get_submatrices(&matrix, 3, 3);

    let mut results = 0;

    for submatrix in &submatrices {
        if match_submatrix(submatrix) {
            results += 1;
        }
    }

    results
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
    use std::fs;

    fn get_input() -> &'static str {
        r#"
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
        .trim()
    }

    fn get_file_input() -> String {
        fs::read_to_string("input.txt").expect("Failed to read input file")
    }

    #[test]
    fn test_part1() {
        let input = get_input();
        let file_input = get_file_input();
        assert_eq!(solve_part1(input), 18);
        assert_eq!(solve_part1(&file_input), 2633);
    }

    #[test]
    fn test_part2() {
        let input = get_input();
        let file_input = get_file_input();
        assert_eq!(solve_part2(input), 9);
        assert_eq!(solve_part2(&file_input), 1936);
    }
}
