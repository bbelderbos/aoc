use std::fs::{self, File};
use std::io::Write;
use std::process::Command;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: aoc_create <day_number>");
        return;
    }

    let day = &args[1];
    let folder_name = format!("day{:02}", day);

    // Check if the folder already exists
    if fs::metadata(&folder_name).is_ok() {
        eprintln!("Folder {} already exists. Use `cargo init` if you need to reinitialize it.", folder_name);
        return;
    }

    // Create the folder and initialize it as a Cargo project
    if let Err(e) = fs::create_dir(&folder_name) {
        eprintln!("Error creating folder {}: {}", folder_name, e);
        return;
    }

    if let Err(e) = Command::new("cargo")
        .arg("init")
        .arg(&folder_name)
        .status()
    {
        eprintln!("Error running cargo init: {}", e);
        return;
    }

    // Write the Advent of Code template code to src/main.rs
    let template_code = r#"use std::fs;

fn parse_input(input: &str) -> Vec<i32> {
    input.lines()
         .map(|line| line.parse::<i32>().unwrap())
         .collect()
}

fn solve_part1(data: &[i32]) -> i32 {
    data.iter().sum()
}

fn solve_part2(data: &[i32]) -> i32 {
    *data.iter().max().unwrap()
}

fn main() {
    let input = fs::read_to_string("input.txt").expect("Failed to read input file");
    let data = parse_input(&input);

    let part1 = solve_part1(&data);
    println!("Part 1: {}", part1);

    let part2 = solve_part2(&data);
    println!("Part 2: {}", part2);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_examples() {
        let example_input = "1\n2\n3\n4\n5";
        let data = parse_input(example_input);

        assert_eq!(solve_part1(&data), 15); // Replace with Part 1 example output
        assert_eq!(solve_part2(&data), 5);  // Replace with Part 2 example output
    }
}
"#;

    let main_file_path = format!("{}/src/main.rs", folder_name);
    if let Err(e) = fs::write(&main_file_path, template_code) {
        eprintln!("Error writing to {}: {}", main_file_path, e);
        return;
    }

    println!("Project for Day {} created successfully with template code!", day);
}

