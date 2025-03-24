import asyncio
import logging
from typing import List
import heapq

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Task:
    def __init__(self, task_id: int, priority: int):
        self.task_id = task_id
        self.priority = priority

    async def execute(self) -> None:
        try:
            await asyncio.sleep(1)  # 模拟任务执行
            logger.info(f"Task {self.task_id} done")
        except Exception as e:
            logger.error(f"Task {self.task_id} failed: {str(e)}")

    def __lt__(self, other):
        return self.priority > other.priority

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        heapq.heappush(self.tasks, task)

    async def execute_tasks(self) -> None:
        while self.tasks:
            task = heapq.heappop(self.tasks)
            await task.execute()

def main():
    manager = TaskManager()
    manager.add_task(Task(1, 1))
    manager.add_task(Task(2, 2))
    
    asyncio.run(manager.execute_tasks())

if __name__ == "__main__":
    main()
