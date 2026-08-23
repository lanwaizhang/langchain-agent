import os
from dotenv import load_dotenv
from rich import print
from SRC.tools.tool import web_search, scrape_url

load_dotenv()

# ===== 测试 1：搜索 + 抓取 =====
def test_web_search_and_scrape():
    query = "深圳今日天气"
    print(f"[bold cyan]🔍 搜索关键词: {query}[/bold cyan]")
    
    search_result = web_search(query)
    print(search_result)
    
    # 解析搜索结果中的第一个 URL
    lines = search_result.split('\n')
    first_url = None
    for line in lines:
        if line.startswith('URL: '):
            first_url = line.replace('URL: ', '').strip()
            break
    
    if first_url:
        print(f"\n[bold green]📄 正在抓取: {first_url}[/bold green]")
        content = scrape_url(first_url)
        print("\n[bold yellow]--- 抓取结果（前800字） ---[/bold yellow]")
        print(content[:800])
    else:
        print("[red]未找到有效 URL[/red]")

# ===== 测试 2：直接抓取指定 URL =====
def test_direct_scrape():
    # 你可以换成任意你想测试的新闻网址
    url = "https://www.bbc.com/zhongwen/simp"
    print(f"[bold cyan]📄 直接抓取: {url}[/bold cyan]")
    content = scrape_url(url)
    print("\n[bold yellow]--- 抓取结果（前600字） ---[/bold yellow]")
    print(content[:600])

if __name__ == "__main__":
    # 运行测试
    test_web_search_and_scrape()
    # 如果想单独测抓取，取消下面注释
    # test_direct_scrape()