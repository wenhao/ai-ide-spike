import asyncio
import logging
import os
from typing import Dict, List, Any
import aiohttp
import aiofiles
from urllib.parse import urlparse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def download_and_save(url: str, max_retries: int = 3) -> bool:
    """
    下载单个URL内容并保存为文件
    
    参数:
        url: 要下载的URL
        max_retries: 最大重试次数
    
    返回:
        bool: 下载是否成功
    """
    # 从URL提取文件名
    parsed_url = urlparse(url)
    hostname = parsed_url.netloc
    filename = f"{hostname}.html"
    
    # 重试逻辑
    for attempt in range(1, max_retries + 1):
        try:
            async with aiohttp.ClientSession() as session:
                # 设置超时，防止长时间阻塞
                async with session.get(url, timeout=10) as response:
                    if response.status != 200:
                        raise aiohttp.ClientError(f"HTTP错误: {response.status}")
                    
                    # 获取响应内容
                    content = await response.text()
                    
                    # 保存内容到文件
                    async with aiofiles.open(filename, 'w', encoding='utf-8') as f:
                        await f.write(content)
                        
                    logger.info(f"成功下载并保存: {url} -> {filename}")
                    return True
                    
        except aiohttp.ClientError as e:
            if attempt < max_retries:
                wait_time = attempt * 2  # 指数退避策略
                logger.warning(f"下载 {url} 失败 (尝试 {attempt}/{max_retries}): {str(e)}. "
                              f"将在 {wait_time} 秒后重试...")
                await asyncio.sleep(wait_time)
            else:
                logger.error(f"下载 {url} 失败，已达到最大重试次数: {str(e)}")
                return False
                
        except asyncio.TimeoutError:
            if attempt < max_retries:
                wait_time = attempt * 2
                logger.warning(f"下载 {url} 超时 (尝试 {attempt}/{max_retries}). "
                              f"将在 {wait_time} 秒后重试...")
                await asyncio.sleep(wait_time)
            else:
                logger.error(f"下载 {url} 失败，已达到最大重试次数: 请求超时")
                return False
                
        except Exception as e:
            if attempt < max_retries:
                wait_time = attempt * 2
                logger.warning(f"下载或保存 {url} 时发生错误 (尝试 {attempt}/{max_retries}): {str(e)}. "
                              f"将在 {wait_time} 秒后重试...")
                await asyncio.sleep(wait_time)
            else:
                logger.error(f"下载或保存 {url} 时发生错误，已达到最大重试次数: {str(e)}")
                return False
    
    return False  # 这行代码实际上不会执行到，但保留它以保持函数完整性

async def download_files(urls: List[str]) -> Dict[str, int]:
    """
    异步下载多个URL的内容并保存为文件
    
    参数:
        urls: URL列表
    
    返回:
        Dict[str, int]: 包含成功和失败计数的字典
    """
    if not urls:
        return {'success': 0, 'failed': 0}
    
    # 创建任务列表
    tasks = [download_and_save(url) for url in urls]
    
    # 等待所有任务完成
    results = await asyncio.gather(*tasks, return_exceptions=False)
    
    # 统计成功和失败的数量
    success_count = sum(1 for result in results if result)
    failed_count = len(results) - success_count
    
    return {
        'success': success_count,
        'failed': failed_count
    }

# 示例使用
async def main():
    urls = [
        'https://example.com',
        'https://example.org',
        'https://invalid.url'  # 这个URL预期会失败
    ]
    
    print(f"开始下载 {len(urls)} 个URL...")
    result = await download_files(urls)
    print(f"下载结果统计: {result}")

if __name__ == "__main__":
    # 创建事件循环并运行主函数
    asyncio.run(main()) 