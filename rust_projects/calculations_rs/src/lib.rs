use tokio::task;
use tokio::sync::Mutex;
use std::sync::Arc;
use std::time::Instant;
use pyo3::prelude::*;


async fn worker(numbers: Arc<Vec<i64>>, start: usize, end: usize, result: Arc<Mutex<Vec<i64>>>) {
    let mut res = result.lock().await;
    for i in start..end {
        res[i] = numbers[i] * numbers[i];
    }
}

async fn main_async(core_count: usize) -> Arc<Mutex<Vec<i64>>> {
    let numbers: Vec<i64> = (0..8000000).collect();
    let result = Arc::new(Mutex::new(vec![0; numbers.len()]));
    let segment = numbers.len() / core_count;
    let mut handles = vec![];
    let numbers = Arc::new(numbers);
    println!("We will process {} numbers, divided in segments of length {}", numbers.len(), segment);
    for i in 0..core_count {
        let start = i * segment;
        let end = if i == core_count - 1 {
            numbers.len()
        } else {
            start + segment
        };
        let numbers = Arc::clone(&numbers);
        let result = Arc::clone(&result);

        let handle = task::spawn(async move {
            worker(numbers, start, end, result).await;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.await.unwrap();
    }

    result
}

#[tokio::main]
async fn main() {
    for &core_count in &[1, 2, 4, 8, 16, 32]{
        let start_time = Instant::now();
        println!("Using {} cores:", core_count);
        let _result = main_async(core_count).await;
        let duration = start_time.elapsed();
        println!("Time taken in rust: {:.2} seconds", duration.as_secs_f64());
    }
}


#[pyfunction]
fn multiply() -> PyResult<isize> {
    println!("Calling main");
    main();
    Ok(0)
}

#[pymodule]
fn calculations_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(multiply, m)?)?;
    Ok(())
}

