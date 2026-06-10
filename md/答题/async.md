```python
async def fetch_all(urls:List[str], max_concurrency:int=10):
    semaphore = asyncio.Semaphore(max_concurrency)
    async def fetch_limited(url:str):
        async with semaphore:
            return await fetch(url)
    return await asyncio.gather(*[fetch_limited(url) for url in urls],return_exceptions=True)
async def main():
    results = await fetch_all(urls)
    for result in results:
        try:
            print(result)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            continue
     files_results = await download_all(urls)
async def download_file(url: str) -> str:
    """假设这个函数已经存在，耗时 2 秒"""
    await asyncio.sleep(2)
    return f"下载完成: {url}"
async def download_all(urls:List[str], max_concurrency:int=10):
    semaphore = asyncio.Semaphore(max_concurrency)
    async def download_limited(url:str):
        async with semaphore:
            return await download_file(url)
    return await asyncio.gather(*[download_limited(url) for url in urls],return_exceptions=True)

    async def fetch_all(urls: List[str]):
    results = await asyncio.gather(
        *[fetch(u) for u in urls],
        return_exceptions=True
    )
    
    # 想打印失败的结果
    for result in results:
        try:
            print(f"成功了: {result}")
           
        except:
             if result is Exception:   # ← 这里有错
                print(f"失败了: {result}")
urls = ["https://a.com", "https://b.com", "https://c.com"]
results = await asyncio.gather(*[fetch(u) for u in urls], return_exceptions=True)

# 你的代码：
for result in results:
    try:
        print(f"成功了: {result}")
    except:
        if isinstance(result, Exception):
            print(f"失败了: {result}")
````
