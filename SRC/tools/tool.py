from langchain.tools import tool
import os
import re
import requests
from dotenv import load_dotenv
from tavily import TavilyClient
from rich import print
from bs4 import BeautifulSoup
from readability import Document
import trafilatura

load_dotenv()

# 初始化 Tavily 客户端
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# ---------- 工具 1：网页搜索 ----------
@tool
def web_search(query: str) -> str:
    """
    搜索网络获取最新信息。适用于查询当前事件、新闻、事实资料等。
    返回包含标题、URL和摘要的搜索结果。
    """
    results = tavily.search(query=query, max_results=3)
    out = []
    for r in results.get('results', []):
        out.append(
            f"Title: {r.get('title', '无标题')}\n"
            f"URL: {r.get('url', '无链接')}\n"
            f"Snippet: {r.get('content', '无摘要')[:300]}\n"
        )
    if not out:
        return "未搜索到相关结果。"
    return "\n---\n".join(out)

# ---------- 工具 2：抓取网页正文 ----------
@tool
def scrape_url(url: str) -> str:
    """
    抓取并提取指定 URL 的清晰可读正文内容。
    采用多种提取策略（trafilatura -> readability -> BeautifulSoup）以提高可靠性。
    适用于需要获取网页详细内容的场景。
    """
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        ),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
    }

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        html = resp.text
    except Exception as e:
        return f"抓取网页失败: {str(e)}"

    # ----- 策略 1：使用 trafilatura（通常效果最好） -----
    try:
        extracted = trafilatura.extract(html, include_comments=False, include_tables=False)
        if extracted and len(extracted.strip()) > 100:
            cleaned = re.sub(r'\n\s*\n', '\n\n', extracted.strip())
            return cleaned
    except Exception:
        pass  # 策略1失败，进入策略2

    # ----- 策略 2：使用 readability-lxml -----
    try:
        doc = Document(html)
        readable_html = doc.summary()
        soup = BeautifulSoup(readable_html, 'html.parser')
        text = soup.get_text(separator='\n')
        cleaned = re.sub(r'\n\s*\n', '\n\n', text.strip())
        if len(cleaned) > 100:
            return cleaned
    except Exception:
        pass  # 策略2失败，进入策略3

    # ----- 策略 3：使用 BeautifulSoup 手动清理 -----
    try:
        soup = BeautifulSoup(html, 'html.parser')
        # 移除脚本和样式标签
        for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
            tag.decompose()
        # 尝试获取正文（优先找 article、main 等标签）
        for selector in ['article', 'main', '.content', '#content', '.post', '.entry']:
            target = soup.select_one(selector)
            if target:
                text = target.get_text(separator='\n')
                cleaned = re.sub(r'\n\s*\n', '\n\n', text.strip())
                if len(cleaned) > 50:
                    return cleaned
        # 如果找不到特定容器，返回整个 body 的文本
        body = soup.body
        if body:
            text = body.get_text(separator='\n')
            cleaned = re.sub(r'\n\s*\n', '\n\n', text.strip())
            if len(cleaned) > 50:
                return cleaned
    except Exception:
        pass

    return "无法从该网页提取可读内容，可能页面结构特殊或需要登录。"