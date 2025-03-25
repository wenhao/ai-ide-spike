import asyncio
import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class Task:
    """
    Represents a single task with an ID and priority.
    Higher priority tasks are executed first.
    """
    def __init__(self, task_id: int, priority: int):
        """
        Initialize a task with an ID and priority.
        
        Args:
            task_id: Unique identifier for the task
            priority: Priority level (higher priority tasks execute first)
        """
        self.task_id = task_id
        self.priority = priority
    
    async def execute(self) -> bool:
        """
        Execute the task asynchronously.
        The sample task simulates a delay of 1 second.
        
        Returns:
            bool: True if the task executed successfully, False otherwise
        """
        try:
            # Simulate some async work with a delay
            await asyncio.sleep(1)
            logger.info(f"Task {self.task_id} done")
            return True
        except Exception as e:
            logger.error(f"Task {self.task_id} failed with error: {str(e)}")
            return False
    
    def __str__(self) -> str:
        return f"Task {self.task_id}"
    
    def __repr__(self) -> str:
        return f"Task(id={self.task_id}, priority={self.priority})"


class TaskManager:
    """
    Manages a queue of tasks and executes them according to priority.
    """
    def __init__(self):
        """Initialize an empty task queue."""
        self.tasks: List[Task] = []
        self.execution_log: List[str] = []
    
    def add_task(self, task: Task) -> None:
        """
        Add a task to the queue.
        
        Args:
            task: The task to add
        """
        self.tasks.append(task)
    
    def _sort_tasks(self) -> None:
        """Sort tasks by priority (highest priority first)."""
        self.tasks.sort(key=lambda task: task.priority, reverse=True)
    
    async def execute_tasks(self) -> List[str]:
        """
        Execute all tasks in order of priority.
        Failed tasks are logged.
        
        Returns:
            List[str]: Execution log
        """
        self._sort_tasks()
        self.execution_log = []
        
        for task in self.tasks:
            try:
                success = await task.execute()
                if success:
                    self.execution_log.append(f"{task} done")
                else:
                    self.execution_log.append(f"{task} failed")
            except Exception as e:
                logger.error(f"Error executing {task}: {str(e)}")
                self.execution_log.append(f"{task} failed with error: {str(e)}")
        
        return self.execution_log
    
    def get_execution_log(self) -> List[str]:
        """
        Get the execution log.
        
        Returns:
            List[str]: The execution log
        """
        return self.execution_log


async def main():
    """Example usage of the task management system."""
    manager = TaskManager()
    manager.add_task(Task(1, 1))  # Lower priority
    manager.add_task(Task(2, 2))  # Higher priority
    
    await manager.execute_tasks()
    
    # Print the execution log
    logger.info(f"Execution log: {manager.get_execution_log()}")


if __name__ == "__main__":
    # Run the main coroutine
    asyncio.run(main())
