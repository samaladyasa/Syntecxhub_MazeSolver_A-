import csv
import os
import tempfile
from collections import deque
from heapq import heappop, heappush
from math import sqrt

from pyamaze import COLOR, agent, maze, textLabel


def heuristic(a, b, mode='manhattan'):
    dr = abs(a[0] - b[0])
    dc = abs(a[1] - b[1])
    if mode == 'euclidean':
        return sqrt(dr * dr + dc * dc)
    return dr + dc


def neighbors(grid, cell):
    rows, cols = len(grid), len(grid[0])
    r, c = cell
    steps = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    out = []
    for dr, dc in steps:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
            out.append((nr, nc))
    return out


def build_path(came_from, goal):
    path = [goal]
    while path[-1] in came_from:
        path.append(came_from[path[-1]])
    path.reverse()
    return path


def a_star(grid, start, goal, mode='manhattan'):
    if not grid or not grid[0]:
        raise ValueError('Grid cannot be empty')

    rows, cols = len(grid), len(grid[0])
    sr, sc = start
    gr, gc = goal

    if not (0 <= sr < rows and 0 <= sc < cols and 0 <= gr < rows and 0 <= gc < cols):
        raise ValueError('Start or goal is outside the grid')
    if grid[sr][sc] == 1 or grid[gr][gc] == 1:
        raise ValueError('Start or goal cannot be a wall')

    open_heap = [(heuristic(start, goal, mode), 0, start)]
    came_from = {}
    g_score = {start: 0}
    explored_set = set()
    explored_order = []

    while open_heap:
        _, cost, current = heappop(open_heap)
        if current in explored_set:
            continue
        explored_set.add(current)
        explored_order.append(current)

        if current == goal:
            return build_path(came_from, goal), explored_order

        for nxt in neighbors(grid, current):
            new_cost = cost + 1
            if new_cost < g_score.get(nxt, float('inf')):
                g_score[nxt] = new_cost
                came_from[nxt] = current
                f = new_cost + heuristic(nxt, goal, mode)
                heappush(open_heap, (f, new_cost, nxt))

    return None, explored_order


def print_grid(grid, start, goal, path=None, explored=None):
    path_cells = set(path or [])
    explored_cells = set(explored or [])

    for r in range(len(grid)):
        row_chars = []
        for c in range(len(grid[0])):
            cell = (r, c)
            if cell == start:
                ch = 'S'
            elif cell == goal:
                ch = 'G'
            elif grid[r][c] == 1:
                ch = '#'
            elif cell in path_cells:
                ch = '*'
            elif cell in explored_cells:
                ch = '+'
            else:
                ch = '.'
            row_chars.append(ch)
        print(' '.join(row_chars))


def plot_grid(
    grid,
    start,
    goal,
    path=None,
    explored=None,
    search_delay_ms=70,
    reverse_delay_ms=85,
    forward_delay_ms=110,
):
    rows, cols = len(grid), len(grid[0])
    path_list = list(path or [])
    explored_list = list(explored or [])

    def to_maze_cell(cell):
        return (cell[0] + 1, cell[1] + 1)

    def to_trace(path_cells):
        if not path_cells or len(path_cells) < 2:
            return {}
        trace = {}
        converted = [to_maze_cell(cell) for cell in path_cells]
        for i in range(len(converted) - 1):
            trace[converted[i]] = converted[i + 1]
        return trace

    def shortest_walk(a, b):
        if a == b:
            return [a]
        q = deque([a])
        parent = {a: None}
        while q:
            cur = q.popleft()
            if cur == b:
                break
            for nxt in neighbors(grid, cur):
                if nxt not in parent:
                    parent[nxt] = cur
                    q.append(nxt)
        if b not in parent:
            return []
        seq = []
        node = b
        while node is not None:
            seq.append(node)
            node = parent[node]
        seq.reverse()
        return seq

    filtered_explored = [cell for cell in explored_list if grid[cell[0]][cell[1]] == 0]
    if not filtered_explored:
        filtered_explored = [start]
    if filtered_explored[0] != start:
        filtered_explored.insert(0, start)

    search_walk = [filtered_explored[0]]
    for cell in filtered_explored[1:]:
        segment = shortest_walk(search_walk[-1], cell)
        if len(segment) > 1:
            search_walk.extend(segment[1:])

    goal_cell = to_maze_cell(goal)
    start_cell = to_maze_cell(start)

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as tmp:
        tmp_path = tmp.name
        writer = csv.writer(tmp)
        writer.writerow(['  cell  ', 'E', 'W', 'N', 'S'])

        for r in range(rows):
            for c in range(cols):
                state = {'E': 0, 'W': 0, 'N': 0, 'S': 0}
                if grid[r][c] == 0:
                    if c + 1 < cols and grid[r][c + 1] == 0:
                        state['E'] = 1
                    if c - 1 >= 0 and grid[r][c - 1] == 0:
                        state['W'] = 1
                    if r - 1 >= 0 and grid[r - 1][c] == 0:
                        state['N'] = 1
                    if r + 1 < rows and grid[r + 1][c] == 0:
                        state['S'] = 1

                writer.writerow([(r + 1, c + 1), state['E'], state['W'], state['N'], state['S']])

    m = maze(rows, cols)
    m.CreateMaze(x=goal_cell[0], y=goal_cell[1], loadMaze=tmp_path, theme=COLOR.dark)
    os.remove(tmp_path)

    path_length = max(len(path_list) - 1, 0) if path_list else 0
    search_length = len(explored or [])
    textLabel(m, 'Star Path Length', path_length)
    textLabel(m, 'A Star Search Length', search_length)
    print(f'Pyamaze view -> Star Path Length: {path_length}')
    print(f'Pyamaze view -> A Star Search Length: {search_length}')

    search_agent = agent(
        m,
        x=start_cell[0],
        y=start_cell[1],
        goal=goal_cell,
        color=COLOR.blue,
        footprints=True,
        filled=True,
    )
    reverse_agent = agent(
        m,
        x=goal_cell[0],
        y=goal_cell[1],
        goal=start_cell,
        color=COLOR.yellow,
        footprints=True,
        filled=True,
    )
    forward_agent = agent(
        m,
        x=start_cell[0],
        y=start_cell[1],
        goal=goal_cell,
        color=COLOR.red,
        footprints=True,
        filled=False,
    )

    search_trace = to_trace(search_walk)
    reverse_trace = to_trace(list(reversed(path_list)))
    forward_trace = to_trace(path_list)

    if search_trace:
        m.tracePath({search_agent: search_trace}, delay=search_delay_ms)

    if reverse_trace:
        m.tracePath({reverse_agent: reverse_trace}, delay=reverse_delay_ms)

    if forward_trace:
        m.tracePath({forward_agent: forward_trace}, delay=forward_delay_ms)
    else:
        m.tracePath({forward_agent: {}}, delay=1)

    m.run()


if __name__ == '__main__':
    grid = [
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    ]
    start = (0, 0)
    goal = (14, 14)

    path, explored = a_star(grid, start, goal, mode='manhattan')

    if path is None:
        print('No path found (goal is unreachable).')
    else:
        print('Shortest path length:', len(path) - 1)
        print('Path:', path)

    print('\nLegend: S=start, G=goal, #=wall, *=path, +=explored, .=free')
    print_grid(grid, start, goal, path, explored)
    plot_grid(
        grid,
        start,
        goal,
        path,
        explored,
        search_delay_ms=70,
        reverse_delay_ms=85,
        forward_delay_ms=110,
    )