# LangChain-Agent

AI research assistant built with LangChain, Tavily and Streamlit.

## Summary

`langchain-agent` 是一个用于自动化研究流水线的示例项目。它将“搜索 → 抓取 → 撰写 → 评估”四个步骤串联起来，借助 LangChain agent 与第三方抓取/搜索工具自动生成结构化研究报告。

## Features

- 基于 Agent 的搜索与阅读（ReAct 风格）
- 多策略网页抓取（trafilatura / readability / BeautifulSoup）
- 报告撰写与自动评审（writer & critic chain）
- 提供命令行与 Streamlit 可视化两种运行方式

## Technologies

- Python 3.10+
- LangChain (langchain, langchain-core, langchain-openai, langchain-community)
- DeepSeek / LangChain OpenAI 接入（通过环境变量配置）
- Tavily（用于搜索）
- Scraping: `requests`, `beautifulsoup4`, `trafilatura`, `readability-lxml`, `lxml`
- Web UI: `streamlit`
- 配置管理: `python-dotenv`

（依赖可在 `requirements.txt` 中查看）

## Quick Install

推荐使用虚拟环境：

```bash
git clone https://github.com/yourname/langchain-agent.git
cd langchain-agent
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Environment Variables

在根目录创建 `.env` 文件（或在系统环境中设置）：

```text
DEEPSEEK_API_KEY=your_deepseek_key
TAVILY_API_KEY=your_tavily_key
# 可选：OPENAI_API_KEY=your_openai_key
```

## Usage

- 运行命令行示例（快速测试）：

```bash
python main.py
```

- 启动 Streamlit Web UI：

```bash
streamlit run app.py
```

Streamlit 页面为 `app.py`，可在浏览器中交互式输入研究主题并查看各步骤输出。

## Architecture (brief)

项目目录中的关键模块：

- `SRC/pipelines/pipeline.py`：流水线编排，按顺序调用搜索、阅读、写作、批评四个环节，并返回 `state` 字典。
- `SRC/agents/agants.py`：构建三类 Agent（search / reader）与写手/评论者 chain，负责与 LLM 交互。
- `SRC/tools/tool.py`：实现外部能力（`web_search`, `scrape_url`），使用 Tavily 和多种解析策略进行网页抓取。

数据流：

Search Agent -> Reader Agent (scrape) -> Writer Chain -> Critic Chain -> 返回报告与评估

## Contributing

欢迎贡献！请先提交 issue 讨论大改动，再发起 pull request。建议遵循以下流程：

1. Fork 仓库
2. 新建分支 `feat/描述` 或 `fix/描述`
3. 提交并发起 PR，描述变更与复现步骤

## License

本仓库默认 MIT（请根据实际需要替换为你想要的许可）。

## Contact

如有问题或合作意向，请在项目仓库中打开 issue。

