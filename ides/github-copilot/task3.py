import aiohttp
import aiofiles
import asyncio
import logging
from urllib.parse import urlparse
from functools import wraps
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('download.log'),
        logging.StreamHandler()
    ]
)

async def retry_decorator(func, retries=3):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        for attempt in range(retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if attempt == retries - 1:
                    logging.error(f"Failed after {retries} attempts: {str(e)}")
                    raise
                logging.warning(f"Attempt {attempt + 1} failed, retrying...")
                await asyncio.sleep(1)
    return wrapper

async def download_and_save(session, url):
    @retry_decorator
    async def _download():
        async with session.get(url) as response:
            response.raise_for_status()
            filename = f"{urlparse(url).netloc}.html"
            async with aiofiles.open(filename, 'w', encoding='utf-8') as f:
                await f.write(await response.text())
            return filename

    return await _download()

async def download_files(urls):
    results = {'success': 0, 'failed': 0}
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(asyncio.create_task(download_and_save(session, url)))
        
        for task in tasks:
            try:
                filename = await task
                logging.info(f"Successfully downloaded and saved to {filename}")
                results['success'] += 1
            except Exception as e:
                logging.error(f"Failed to process URL: {str(e)}")
                results['failed'] += 1
    
    return results

if __name__ == "__main__":
    urls = [
        'https://example.com',
        'https://example.org',
        'https://invalid.url'
    ]
    
    async def main():
        result = await download_files(urls)
        print(result)
    
    asyncio.run(main())
