### 场景 2：上下文理解与系统架构
- 维度：测试工具理解多组件上下文并设计模块化系统的能力。
- 任务：  
用 Python 设计一个任务管理系统，支持以下功能：

    - a. TaskManager 类管理任务队列。
    - b. Task 类表示单个任务，包含 id、priority 和 execute 方法（异步）。
    - c. 任务按优先级排序并依次执行，失败的任务记录到日志。 
示例任务：模拟延迟 1 秒后返回结果。
- 输入示例：
```python
manager = TaskManager()
manager.add_task(Task(1, 1))
manager.add_task(Task(2, 2))
manager.execute_tasks()
```
- 期望输出：日志记录 [Task 2 done, Task 1 done]。
- 考核点：
    - 是否正确理解并实现多类协作的上下文。
    - 模块化设计的清晰度和可扩展性。
    - 异步任务调度和优先级排序的准确性。 