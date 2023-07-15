use std::collections::HashMap;

fn energy_level(
    x: u16,
    y: u16,
    k: u16,
    cache: &mut HashMap<(u16, u16, u16), u16>
) -> u16 {
  if let Some(result) = cache.get(&(x, y, k)) {
    return *result;
  }

  let result: u16;

  if x == 0 {
    result = (y + 1) % 32768;
  } else if y == 0 {
    result = energy_level(x - 1, k, k, cache);
  } else {
    let new_y = energy_level(x, y - 1, k, cache);
    result = energy_level(x - 1, new_y, k, cache);
  }

    cache.insert((x, y, k), result);
    result
}


fn main() {
  const X: u16 = 4;
  const Y: u16 = 1;

  for k in 0..32768 {
    println!("calculating energy_level({X}, {Y}, {k})");

    let mut cache: HashMap<(u16, u16, u16), u16> = HashMap::new();

    let result = energy_level(X, Y, k, &mut cache);

    println!("energy_level({X}, {Y}, {k}) = {result}");

    if result == 6 {
        println!("energy level should be {k}");
        break;
    }
  }
}
