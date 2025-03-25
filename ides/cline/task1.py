#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
任务1：逻辑推理与算法设计
使用BFS（广度优先搜索）算法计算迷宫从左上角到右下角的最短路径长度
"""

from collections import deque


def shortest_path(maze):
    """
    使用BFS查找迷宫的最短路径长度
    
    参数:
        maze: 二维整数数组，0表示通路，1表示墙
    
    返回:
        int: 最短路径长度，若无路径则返回-1
    """
    # 输入验证
    if not maze or not isinstance(maze, list):
        return -1
    if not all(isinstance(row, list) for row in maze):
        return -1
    
    rows = len(maze)
    if rows == 0:
        return -1
    
    cols = len(maze[0])
    if cols == 0:
        return -1
    
    # 检查所有行的长度是否一致
    if any(len(row) != cols for row in maze):
        return -1
    
    # 检查起点和终点是否为墙
    if maze[0][0] == 1 or maze[rows-1][cols-1] == 1:
        return -1
    
    # BFS实现
    queue = deque([(0, 0, 1)])  # (行, 列, 路径长度)
    visited = {(0, 0)}
    
    # 四个方向: 右, 下, 左, 上
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        row, col, length = queue.popleft()
        
        # 如果到达终点
        if row == rows - 1 and col == cols - 1:
            return length
        
        # 探索四个方向
        for d_row, d_col in directions:
            new_row, new_col = row + d_row, col + d_col
            
            # 检查新位置是否有效
            if (0 <= new_row < rows and 
                0 <= new_col < cols and 
                maze[new_row][new_col] == 0 and 
                (new_row, new_col) not in visited):
                
                visited.add((new_row, new_col))
                queue.append((new_row, new_col, length + 1))
    
    # 如果无法到达终点
    return -1


# 测试代码
if __name__ == "__main__":
    # 测试用例1: 示例输入
    test_maze1 = [
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]
    print(f"测试用例1结果: {shortest_path(test_maze1)}")  # 应输出4
    
    # 测试用例2: 无路径
    test_maze2 = [
        [0, 1, 0],
        [1, 1, 0],
        [0, 1, 0]
    ]
    print(f"测试用例2结果: {shortest_path(test_maze2)}")  # 应输出-1
    
    # 测试用例3: 复杂迷宫
    test_maze3 = [
        [0, 0, 0, 0, 1, 0],
        [1, 1, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 1, 1, 0, 0, 1],
        [0, 0, 0, 0, 0, 0]
    ]
    print(f"测试用例3结果: {shortest_path(test_maze3)}")  # 应输出10
    
    # 测试用例4: 边界情况 - 空迷宫
    test_maze4 = []
    print(f"测试用例4结果: {shortest_path(test_maze4)}")  # 应输出-1
    
    # 测试用例5: 最小迷宫
    test_maze5 = [[0]]
    print(f"测试用例5结果: {shortest_path(test_maze5)}")  # 应输出1
