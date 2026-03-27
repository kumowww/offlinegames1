extern crate piston_window;
extern crate rand;

use piston_window::*;
use rand::Rng;

const GRID_SIZE: f64 = 20.0;
const CANVAS_SIZE: u32 = 400; // 20x20 pixels

struct Snake {
    body: Vec<(i32, i32)>,
    dir: (i32, i32),
}

fn main() {
    let mut window: PistonWindow = WindowSettings::new("Rust Snake", [CANVAS_SIZE, CANVAS_SIZE])
        .exit_on_esc(true).build().unwrap();

    let mut snake = Snake { body: vec![(10, 10)], dir: (1, 0) };
    let mut food = (5, 5);
    let mut timer = 0.0;

    while let Some(event) = window.next() {
        if let Some(Button::Keyboard(key)) = event.press_args() {
            snake.dir = match key {
                Key::Up if snake.dir.1 != 1 => (0, -1),
                Key::Down if snake.dir.1 != -1 => (0, 1),
                Key::Left if snake.dir.0 != 1 => (-1, 0),
                Key::Right if snake.dir.0 != -1 => (1, 0),
                _ => snake.dir,
            };
        }

        event.update(|args| {
            timer += args.dt;
            if timer > 0.15 {
                timer = 0.0;
                let head = snake.body[0];
                let new_head = (head.0 + snake.dir.0, head.1 + snake.dir.1);

                // Checking boundaries and collisions
                if new_head.0 < 0 || new_head.0 >= 20 || new_head.1 < 0 || new_head.1 >= 20 
                   || snake.body.contains(&new_head) {
                    snake.body = vec![(10, 10)]; // Reset
                } else {
                    snake.body.insert(0, new_head);
                    if new_head == food {
                        food = (rand::thread_rng().gen_range(0..20), rand::thread_rng().gen_range(0..20));
                    } else {
                        snake.body.pop();
                    }
                }
            }
        });

        window.draw_2d(&event, |c, g, _| {
            clear([0.0, 0.0, 0.0, 1.0], g); // Black background 0_0
            
            // EAT
            ellipse([1.0, 1.0, 1.0, 1.0], 
                    [food.0 as f64 * GRID_SIZE, food.1 as f64 * GRID_SIZE, GRID_SIZE, GRID_SIZE], 
                    c.transform, g);

            // Snake (white squares)
            for part in &snake.body {
                rectangle([1.0, 1.0, 1.0, 1.0],
                          [part.0 as f64 * GRID_SIZE, part.1 as f64 * GRID_SIZE, GRID_SIZE, GRID_SIZE],
                          c.transform, g);
            }
        });
    }
}