import os
from langchain.agents import create_react_agent, AgentExecutor 
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain import hub                     # 新增：用于拉取标准模板
from SRC.tools.tool import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

# Model Initialization
llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    openai_api_base="https://api.deepseek.com/v1",  # 关键：指向 DeepSeek
    temperature=0
)

# ---------- 1st Agent : Search Agent ----------
def build_search_agent():
    # 使用 Hub 上的 ReAct 标准模板
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=[web_search], prompt=prompt)
    return AgentExecutor(
            agent=agent,
            tools=[web_search],
            verbose=True,
            handle_parsing_errors=True
        )

# ---------- 2nd Agent : Reader Agent ----------
def build_reader_agent():
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=[scrape_url], prompt=prompt)
    return AgentExecutor(
        agent=agent,
        tools=[scrape_url],
        verbose=True,
        handle_parsing_errors=True
    )

# ---------- Writer Chain ----------
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的研究报告撰写专家。请写出清晰、结构严谨、有洞见的报告。"),
    ("human", """请根据以下主题和研究资料，撰写一份详细的研究报告。

主题: {topic}

研究资料: {research}

报告结构要求：
- 引言
- 核心发现（至少 3 个要点，每个要点需详细展开）
- 结论
- 参考资料（列出研究中找到的所有 URL）

请确保内容详实、专业、基于事实。"""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# ---------- Critic Chain ----------
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位犀利且建设性的研究评论家。请诚实、具体地指出问题。"),
    ("human", """请严格评审以下研究报告，并给出评分和改进建议。

报告内容:
{report}

请按以下格式回复：

评分: X/10
优点:
- ...
- ...

待改进之处:
- ...
- ...

一句话总结:
- ..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()