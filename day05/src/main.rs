use std::collections::HashMap;
use std::fs;

fn extract_rules_and_orders(input: &str) -> (Vec<(i32, i32)>, Vec<Vec<i32>>) {
    let sections: Vec<&str> = input.trim().split("\n\n").collect();

    if sections.len() != 2 {
        panic!("Input should contain two sections separated by a double newline.");
    }

    let rules: Vec<(i32, i32)> = sections[0]
        .lines()
        .map(|line| {
            let parts: Vec<i32> = line
                .split('|')
                .filter_map(|x| x.parse::<i32>().ok())
                .collect();
            if parts.len() != 2 {
                panic!("Invalid rule format: {}", line);
            }
            (parts[0], parts[1])
        })
        .collect();

    let orders: Vec<Vec<i32>> = sections[1]
        .lines()
        .map(|line| {
            line.split(',')
                .filter_map(|x| x.parse::<i32>().ok())
                .collect()
        })
        .collect();

    (rules, orders)
}

fn is_valid_order(order: &Vec<i32>, rules: &Vec<(i32, i32)>) -> bool {
    let index_map: HashMap<i32, usize> = order.iter().enumerate().map(|(i, &v)| (v, i)).collect();

    for &(before, after) in rules {
        if let (Some(&before_idx), Some(&after_idx)) =
            (index_map.get(&before), index_map.get(&after))
        {
            if before_idx > after_idx {
                return false;
            }
        }
    }

    true
}

fn solve_part1(input: &str) -> i32 {
    let (rules, orders) = extract_rules_and_orders(input);

    let mut valid_orders: Vec<Vec<i32>> = Vec::new();
    for order in orders {
        if is_valid_order(&order, &rules) {
            valid_orders.push(order.clone());
        }
    }

    let middle_sum: i32 = valid_orders
        .iter()
        .map(|order| order[order.len() / 2]) // Directly access the middle value
        .sum();

    middle_sum
}

fn fix_order(order: &Vec<i32>, rules: &Vec<(i32, i32)>) -> (bool, Vec<i32>) {
    let mut fixed_order = order.clone();
    let mut has_changed = false;

    for _ in 0..rules.len() {
        // Repeat to propagate changes fully
        let mut updated = false;

        for &(before, after) in rules {
            if let (Some(before_idx), Some(after_idx)) = (
                fixed_order.iter().position(|&x| x == before),
                fixed_order.iter().position(|&x| x == after),
            ) {
                if before_idx > after_idx {
                    fixed_order.swap(before_idx, after_idx);
                    updated = true;
                    has_changed = true;
                }
            }
        }

        if !updated {
            break; // Exit early if no changes are made
        }
    }

    (has_changed, fixed_order)
}

fn solve_part2(input: &str) -> i32 {
    let (rules, orders) = extract_rules_and_orders(input);

    let mut fixed_orders: Vec<Vec<i32>> = Vec::new();

    for order in orders {
        let (has_changed, fixed_order) = fix_order(&order, &rules);
        if has_changed {
            fixed_orders.push(fixed_order);
        }
    }

    let middle_sum: i32 = fixed_orders
        .iter()
        .map(|order| order[order.len() / 2])
        .sum();

    middle_sum
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
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
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
        assert_eq!(solve_part1(input), 143);
        assert_eq!(solve_part1(&file_input), 6041);
    }

    #[test]
    fn test_part2() {
        let input = get_input();
        let file_input = get_file_input();
        assert_eq!(solve_part2(input), 123);
        assert_eq!(solve_part2(&file_input), 4884);
    }
}
