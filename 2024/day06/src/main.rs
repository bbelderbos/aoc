use std::collections::HashSet;
use std::fs;

#[derive(Debug, Clone, Copy)]
enum Direction {
    North,
    East,
    South,
    West,
}

impl Direction {
    fn delta(&self) -> (i32, i32) {
        match self {
            Direction::North => (-1, 0),
            Direction::East => (0, 1),
            Direction::South => (1, 0),
            Direction::West => (0, -1),
        }
    }
}

fn parse_grid(input: &str) -> Vec<Vec<char>> {
    input.lines().map(|line| line.chars().collect()).collect()
}

fn find_in_grid(grid: &[Vec<char>], target: char) -> (i32, i32) {
    for (i, row) in grid.iter().enumerate() {
        for (j, &cell) in row.iter().enumerate() {
            if cell == target {
                return (i as i32, j as i32);
            }
        }
    }
    panic!("Target not found in grid");
}

fn traverse_grid(grid: &[Vec<char>], start: (i32, i32)) -> usize {
    let directions = vec![
        Direction::North,
        Direction::East,
        Direction::South,
        Direction::West,
    ];

    let mut cycling_directions = directions.iter().cycle();
    let mut direction = cycling_directions.next().unwrap();

    let mut processed = HashSet::new();
    let (mut i, mut j) = start;

    loop {
        processed.insert((i, j));
        let next_position = (i + direction.delta().0, j + direction.delta().1);

        if let Some(&cell) = grid
            .get(next_position.0 as usize)
            .and_then(|row| row.get(next_position.1 as usize))
        {
            if cell == '#' {
                direction = cycling_directions.next().unwrap();
                continue;
            }
        } else {
            return processed.len(); // out of bounds = done
        }

        (i, j) = next_position;
    }
}

fn solve_part1(input: &str) -> usize {
    let data = parse_grid(input);
    let start = find_in_grid(&data, '^');
    traverse_grid(&data, start)
}

// fn solve_part2(input: &str) -> i32 {
//     todo!();
// }

fn main() {
    let input = fs::read_to_string("input.txt").expect("Failed to read input file");

    let part1 = solve_part1(&input);
    println!("Part 1: {}", part1);

    // let part2 = solve_part2(data);
    // println!("Part 2: {}", part2);
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    fn get_input() -> &'static str {
        r#"....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."#
            .trim()
    }

    fn get_file_input() -> String {
        fs::read_to_string("input.txt").expect("Failed to read input file")
    }

    #[test]
    fn test_part1() {
        let input = get_input();
        let file_input = get_file_input();
        assert_eq!(solve_part1(input), 41);
        assert_eq!(solve_part1(&file_input), 4758);
    }

    /*#[test]
    fn test_part2() {
        let input = get_input();
        let file_input = get_file_input();
        assert_eq!(solve_part2(input), 1);
        assert_eq!(solve_part2(&file_input), 1);
    }*/
}
