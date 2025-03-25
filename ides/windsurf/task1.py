from collections import deque

def shortest_path(maze):
    if not maze or not maze[0]:
        return -1
    
    n, m = len(maze), len(maze[0])
    if maze[0][0] == 1 or maze[n-1][m-1] == 1:
        return -1
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = deque([(0, 0, 0)])
    visited = [[False] * m for _ in range(n)]
    visited[0][0] = True
    
    while queue:
        x, y, steps = queue.popleft()
        if x == n - 1 and y == m - 1:
            return steps
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and maze[nx][ny] == 0 and not visited[nx][ny]:
                visited[nx][ny] = True
                queue.append((nx, ny, steps + 1))
    
    return -1

if __name__ == '__main__':
    # Test case 1: Valid path
    maze1 = [
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]
    print(shortest_path(maze1))  # Expected: 4
    
    # Test case 2: No path
    maze2 = [
        [0, 1, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]
    print(shortest_path(maze2))  # Expected: -1
    
    # Test case 3: Start or end blocked
    maze3 = [
        [1, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    print(shortest_path(maze3))  # Expected: -1
    
    # Test case 4: Empty maze
    print(shortest_path([]))  # Expected: -1
