from collections import deque
from typing import List, Tuple

def find_shortest_path(maze: List[List[int]]) -> int:
    """
    使用广度优先搜索(BFS)找到从迷宫左上角到右下角的最短路径长度
    
    参数:
        maze: 二维整数数组，0表示通路，1表示墙
        
    返回:
        最短路径长度，若无路径则返回-1
    """
    # 检查输入合法性
    if not maze or not maze[0]:
        return -1
    
    rows, cols = len(maze), len(maze[0])
    
    # 检查起点和终点是否为墙
    if maze[0][0] == 1 or maze[rows-1][cols-1] == 1:
        return -1
    
    # 定义方向: 上、右、下、左
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    # 初始化队列和访问标记
    queue = deque([(0, 0, 1)])  # (行, 列, 路径长度)
    visited = set([(0, 0)])
    
    while queue:
        row, col, path_len = queue.popleft()
        
        # 如果到达终点
        if row == rows - 1 and col == cols - 1:
            return path_len
        
        # 尝试四个方向
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # 检查是否在迷宫范围内且是通路且未访问过
            if (0 <= new_row < rows and 
                0 <= new_col < cols and 
                maze[new_row][new_col] == 0 and 
                (new_row, new_col) not in visited):
                
                queue.append((new_row, new_col, path_len + 1))
                visited.add((new_row, new_col))
    
    # 如果无法到达终点
    return -1

# 测试示例
if __name__ == "__main__":
    test_maze = [
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]
    print(f"最短路径长度: {find_shortest_path(test_maze)}")  # 预期输出: 4
    
    # 没有路径的情况
    no_path_maze = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0]
    ]
    print(f"无路径情况: {find_shortest_path(no_path_maze)}")  # 预期输出: -1 