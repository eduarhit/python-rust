use std::thread;
use std::time::{Duration, Instant};
use pyo3::prelude::*;

fn calc_square(numbers: Vec<i32>) -> Vec<i32> {
    let mut result = Vec::new();
    for n in numbers {
        result.push(n * n);
//         thread::sleep(Duration::from_millis(1));
    }
    result
}

fn calc_cube(numbers: Vec<i32>) -> Vec<i32> {
    let mut result = Vec::new();
    for n in numbers {
        result.push(n * n * n);
//         thread::sleep(Duration::from_millis(1));
    }
    result
}

fn main_task() {
    let core_count = 8;
    let iterations = 4096;
    let numbers: Vec<i32> = (1..10000).collect();
    let mut handles = Vec::new();

    for _ in 0..iterations {
        let numbers_clone = numbers.clone();
        let handle_square = thread::spawn({
            let numbers_clone = numbers_clone.clone();
            move || calc_square(numbers_clone)
        });
        let handle_cube = thread::spawn({
            let numbers_clone = numbers_clone.clone();
            move || calc_cube(numbers_clone)
        });
        handles.push(handle_square);
        handles.push(handle_cube);
    }

    for handle in handles {
        let _ = handle.join().unwrap();
    }
}

#[pyfunction]
fn multiply() -> PyResult<isize> {
    let start = Instant::now();
    main_task();
    let end = Instant::now();
    println!("Execution Time Multi thread Rust: {:?}", end.duration_since(start));
    Ok(0)
}

#[pymodule]
fn calculations_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(multiply, m)?)?;
    Ok(())
}