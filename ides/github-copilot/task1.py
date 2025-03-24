from collections import deque
from typing import List

def find_shortest_path(maze: List[List[int]]) -> int:
    if not maze or not maze[0]:
        return -1
    
    rows, cols = len(maze), len(maze[0])
    if maze[0][0] == 1 or maze[rows-1][cols-1] == 1:
        return -1

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = deque([(0, 0, 0)])  # (row, col, distance)
    visited = {(0, 0)}

    while queue:
        row, col, distance = queue.popleft()
        if row == rows - 1 and col == cols - 1:
            return distance

        for dx, dy in directions:
            new_row, new_col = row + dx, col + dy
            if (0 <= new_row < rows and 
                0 <= new_col < cols and 
                maze[new_row][new_col] == 0 and 
                (new_row, new_col) not in visited):
                visited.add((new_row, new_col))
                queue.append((new_row, new_col, distance + 1))
    
    return -1

# 测试用例
def test_find_shortest_path():
    test_cases = [
        {
            'maze': [
                [0,0,0],
                [1,1,0],
                [0,0,0]
            ],
            'expected': 4
        },
        {
            'maze': [
                [0,1],
                [1,0]
            ],
            'expected': -1
        },
        {
            'maze': [
                [0]
            ],
            'expected': 0
        }
    ]

    for i, test in enumerate(test_cases, 1):
        result = find_shortest_path(test['maze'])
        assert result == test['expected'], f"测试用例 {i} 失败: 期望 {test['expected']}, 得到 {result}"
        print(f"测试用例 {i} 通过")

if __name__ == "__main__":
    test_find_shortest_path()
