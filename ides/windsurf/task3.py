import asyncio
import logging
import os
import re
from typing import Dict, List, Tuple
from urllib.parse import urlparse

import aiohttp
import aiofiles

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('download_errors.log')
    ]
)
logger = logging.getLogger('url_downloader')

MAX_RETRIES = 3
TIMEOUT = 30  # seconds


async def download_url(session: aiohttp.ClientSession, url: str, retry_count: int = 0) -> Tuple[str, bytes, bool]:
    """
    Download content from a URL with retry logic.
    
    Args:
        session: The aiohttp client session
        url: The URL to download
        retry_count: Current retry attempt
        
    Returns:
        Tuple containing the filename, content and success status
    """
    try:
        # Extract domain for the filename
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        # Clean up domain for filename (remove port if present)
        filename = domain.split(':')[0] + '.html'
        
        # Download with timeout
        async with session.get(url, timeout=TIMEOUT) as response:
            if response.status != 200:
                raise aiohttp.ClientResponseError(
                    response.request_info,
                    response.history,
                    status=response.status,
                    message=f"HTTP Error {response.status}: {response.reason}"
                )
            
            content = await response.read()
            return filename, content, True
            
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        # Handle network-related errors with retry logic
        if retry_count < MAX_RETRIES:
            logger.warning(f"Download failed for {url}. Retrying ({retry_count + 1}/{MAX_RETRIES})... Error: {str(e)}")
            # Exponential backoff: 1s, 2s, 4s
            await asyncio.sleep(2 ** retry_count)
            return await download_url(session, url, retry_count + 1)
        else:
            logger.error(f"Failed to download {url} after {MAX_RETRIES} attempts. Error: {str(e)}")
            return url, b'', False
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error downloading {url}: {str(e)}")
        return url, b'', False


async def save_file(filename: str, content: bytes) -> bool:
    """
    Save content to a file.
    
    Args:
        filename: The name of the file to save
        content: The content to save
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        async with aiofiles.open(filename, 'wb') as f:
            await f.write(content)
        return True
    except (IOError, PermissionError) as e:
        logger.error(f"File write error for {filename}: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error saving {filename}: {str(e)}")
        return False


async def download_files(urls: List[str]) -> Dict[str, int]:
    """
    Download multiple files from URLs concurrently.
    
    Args:
        urls: List of URLs to download
        
    Returns:
        Dict with counts of successful and failed downloads
    """
    results = {'success': 0, 'failed': 0}
    
    # Use a connection pooling session
    async with aiohttp.ClientSession() as session:
        download_tasks = []
        
        # Create download tasks
        for url in urls:
            if not url.startswith(('http://', 'https://')):
                logger.warning(f"Invalid URL format: {url}. Skipping.")
                results['failed'] += 1
                continue
                
            download_tasks.append(download_url(session, url))
        
        # Wait for all downloads to complete
        if download_tasks:
            downloads = await asyncio.gather(*download_tasks)
            
            # Process downloads and save to files
            for filename, content, success in downloads:
                if success and content:
                    if await save_file(filename, content):
                        logger.info(f"Successfully saved {filename}")
                        results['success'] += 1
                    else:
                        logger.error(f"Failed to save {filename}")
                        results['failed'] += 1
                else:
                    results['failed'] += 1
    
    logger.info(f"Download summary: {results}")
    return results


async def main():
    """Example usage of the download_files function."""
    urls = [
        'https://example.com',
        'https://example.org',
        'https://invalid.url'  # This URL will fail
    ]
    
    result = await download_files(urls)
    print(f"Download results: {result}")


if __name__ == "__main__":
    asyncio.run(main())
