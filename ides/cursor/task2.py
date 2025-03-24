import asyncio
import logging
from typing import List, Optional
import time
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Task:
    """表示单个任务的类，包含id、优先级和异步执行方法"""
    
    def __init__(self, task_id: int, priority: int):
        """
        初始化任务
        
        参数:
            task_id: 任务ID
            priority: 任务优先级（数字越大优先级越高）
        """
        self.task_id = task_id
        self.priority = priority
    
    async def execute(self) -> bool:
        """
        异步执行任务
        
        返回:
            bool: 任务执行是否成功
        """
        try:
            # 模拟延迟1秒后返回结果
            await asyncio.sleep(1)
            logger.info(f"Task {self.task_id} done")
            return True
        except Exception as e:
            logger.error(f"Task {self.task_id} failed: {str(e)}")
            return False
    
    def __lt__(self, other):
        """用于优先级比较"""
        if not isinstance(other, Task):
            return NotImplemented
        return self.priority > other.priority  # 优先级高的排在前面
    
    def __repr__(self):
        return f"Task(id={self.task_id}, priority={self.priority})"


class TaskManager:
    """管理任务队列的类"""
    
    def __init__(self):
        """初始化任务管理器"""
        self.tasks: List[Task] = []
        self.results = []
    
    def add_task(self, task: Task) -> None:
        """
        添加任务到队列
        
        参数:
            task: 要添加的任务
        """
        self.tasks.append(task)
    
    def get_tasks(self) -> List[Task]:
        """
        获取所有任务
        
        返回:
            List[Task]: 任务列表
        """
        return self.tasks
    
    async def _execute_task(self, task: Task) -> None:
        """
        执行单个任务并记录结果
        
        参数:
            task: 要执行的任务
        """
        result = await task.execute()
        if result:
            self.results.append(f"Task {task.task_id} done")
        else:
            self.results.append(f"Task {task.task_id} failed")
    
    async def _execute_all_tasks(self) -> None:
        """异步执行所有任务"""
        # 按优先级排序任务
        sorted_tasks = sorted(self.tasks)
        
        # 创建任务列表
        tasks = [self._execute_task(task) for task in sorted_tasks]
        
        # 等待所有任务完成
        await asyncio.gather(*tasks)
    
    def execute_tasks(self) -> List[str]:
        """
        执行所有任务并返回结果
        
        返回:
            List[str]: 执行结果列表
        """
        # 清空之前的结果
        self.results = []
        
        # 创建事件循环
        loop = asyncio.get_event_loop()
        try:
            # 在事件循环中执行所有任务
            loop.run_until_complete(self._execute_all_tasks())
        except Exception as e:
            logger.error(f"Error executing tasks: {str(e)}")
        
        return self.results


# 示例使用
if __name__ == "__main__":
    manager = TaskManager()
    manager.add_task(Task(1, 1))  # ID=1，优先级=1
    manager.add_task(Task(2, 2))  # ID=2，优先级=2（更高）
    
    print("开始执行任务...")
    results = manager.execute_tasks()
    print(f"任务执行结果: {results}")
    # 预期输出中的日志顺序: [Task 2 done, Task 1 done] 