### 场景 3：错误处理与健壮性
- 维度：测试工具在异常处理和系统健壮性设计上的能力。
- 任务：  
用 Python 编写一个函数，接受一个 URL 列表，异步下载每个 URL 的内容并保存为文件。若某个下载失败，重试 3 次后仍失败则记录错误日志，最终返回成功和失败的统计。使用 aiohttp 和 aiofiles。
- 输入示例：
```python
urls = [
    'https://example.com',
    'https://example.org',
    'https://invalid.url'
]
result = await download_files(urls)
```
- 期望输出：
    文件保存：example.com.html, example.org.html
    返回：{ 'success': 2, 'failed': 1 }
- 考核点：
    - 是否实现重试逻辑和错误日志记录。
    - 对网络错误、文件写入失败等异常的处理能力。
    - 返回结果的结构化和完整性。 