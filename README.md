# Syntecxhub_MazeSolver_A*
# 🧭 A* Maze Solver 

## 📌 Overview

This project implements the **A*** pathfinding algorithm in a **single Python file**, designed to find the shortest path in a 2D grid maze.

It supports:

* Grid-based maze representation
* Manhattan and Euclidean heuristics
* Detection of unreachable goals
* Console visualization
* Interactive visualization using **Pyamaze**

---

## 🚀 Features

* ✅ Fully self-contained (single `.py` file)
* ✅ A* algorithm using priority queue (`heapq`)
* ✅ Heuristic selection:

  * Manhattan (default)
  * Euclidean
* ✅ Tracks explored nodes
* ✅ Returns shortest path
* ✅ Handles unreachable cases gracefully
* ✅ Console-based grid output
* ✅ Animated visualization using Pyamaze

---

## 🧱 Grid Representation

The maze is defined as a 2D list:

* `0` → Free cell (walkable)
* `1` → Wall (blocked)

Example:

```python
grid = [
    [0, 0, 1],
    [1, 0, 0],
    [1, 1, 0]
]
```

Coordinates:

* `(row, col)` format
* Top-left = `(0,0)`

---

## 🧠 Algorithm Details

### A* Formula

* `g(n)` → cost from start
* `h(n)` → heuristic estimate
* `f(n) = g(n) + h(n)`

The algorithm:

1. Uses a **min-heap (priority queue)**
2. Expands lowest `f(n)` node
3. Updates neighbors
4. Stops when goal is reached or no path exists

---

## 📏 Heuristics

### Manhattan Distance (default)

Best for 4-direction movement:

```
h(n) = |x1 - x2| + |y1 - y2|
```

### Euclidean Distance

```
h(n) = sqrt((x1 - x2)^2 + (y1 - y2)^2)
```

---

## 📦 Requirements

Install dependency:

```bash
pip install pyamaze
```

---

## ▶️ How to Run

Simply run the script:

```bash
python your_file_name.py
```

---

## 🖥️ Output

### Console Output

* Shortest path length
* Path coordinates
* Grid visualization with:

| Symbol | Meaning        |
| ------ | -------------- |
| `S`    | Start          |
| `G`    | Goal           |
| `#`    | Wall           |
| `*`    | Final path     |
| `+`    | Explored nodes |
| `.`    | Free space     |

---

## 📊 Visualization (Pyamaze)

The program generates an animated maze showing:

* 🔵 Search exploration
* 🟡 Reverse path trace
* 🔴 Final shortest path

Also displays:

* Path length
* Number of explored nodes

---

## ⚠️ Edge Cases Handled

* Empty grid
* Start/goal out of bounds
* Start or goal on a wall
* No possible path

---

## 🧩 Code Structure (Single File)

### Core Functions

* `heuristic()` → computes distance
* `neighbors()` → valid moves
* `a_star()` → main algorithm
* `build_path()` → reconstruct path

### Visualization

* `print_grid()` → console output
* `plot_grid()` → Pyamaze animation

### Entry Point

```python
if __name__ == '__main__':
```

---

## 🔧 Customization

You can easily modify:

* Grid layout
* Start and goal positions
* Heuristic type:

```python
mode='euclidean'
```

* Visualization speed:

```python
search_delay_ms
reverse_delay_ms
forward_delay_ms
```

---

## 🏁 Example Result

```
Shortest path length: 28
Path: [(0,0), ..., (14,14)]
```

---

## 📚 Learning Outcomes

* Understanding A* search
* Heuristic optimization
* Graph traversal techniques
* Visualization of search algorithms

---

## 🚧 Future Improvements

* Diagonal movement support
* Weighted grids
* GUI using Tkinter/Pygame
* Real-time interactive maze editing

---

## 📜 License

MIT License — free to use and modify.

---

## 🤝 Contribution

Feel free to fork, improve, and submit pull requests!

---

## 💡 Summary

A clean, single-file implementation of A* with both **algorithmic clarity** and **visual demonstration**, making it ideal for learning and showcasing pathfinding techniques.
