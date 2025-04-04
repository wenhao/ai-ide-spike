### 场景 5：创造性问题解决与复杂需求
- 维度：测试工具在理解复杂需求并提供创新解决方案上的能力。
- 任务：  
用 Python 编写一个命令行工具，支持解析用户输入的数学表达式（例如 2 + 3 * 4），并计算结果。支持加、减、乘、除和括号，处理非法输入时提供友好提示。额外要求：实现一个缓存机制，重复表达式直接返回缓存结果。
- 输入示例：
```python
calc("2 + 3 * 4")    # 第一次计算
calc("2 + 3 * 4")    # 使用缓存
calc("(2 + 3) * 4")  # 新表达式
calc("2 + a")        # 非法输入
```
- 期望输出：正确计算结果并缓存重复输入。
- 考核点：
    - 是否正确解析表达式（例如使用逆波兰表示法或递归下降）。
    - 缓存机制的有效性和边界处理。
    - 用户友好的错误提示和创造性实现。 