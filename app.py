import streamlit as st
from SRC.pipelines.pipeline import run_research_pipeline

# 页面配置
st.set_page_config(page_title="AI 研究助手", page_icon="📚", layout="wide")
st.title("📚 AI 研究助手")
st.markdown("输入一个研究主题，我将自动执行：**搜索 → 阅读 → 撰写报告 → 评估**")

# 输入区域
topic = st.text_input("🔍 输入研究主题", placeholder="例如：人工智能在医疗领域的应用")

if st.button("🚀 开始研究", type="primary") and topic:
    with st.spinner("🧠 研究流水线运行中，请稍候..."):
        try:
            # 运行流水线，获取结果
            state = run_research_pipeline(topic)
        except Exception as e:
            st.error(f"❌ 运行出错：{e}")
            st.stop()

    # 结果展示
    st.success("✅ 研究完成！")

    # 使用列布局展示步骤
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("🔎 1. 搜索结果（摘要）", expanded=True):
            st.write(state.get("search_results", "无搜索结果"))

        with st.expander("📄 2. 抓取内容（正文）", expanded=True):
            st.write(state.get("scraped_content", "无抓取内容"))

    with col2:
        with st.expander("📝 3. 最终报告", expanded=True):
            st.markdown(state.get("report", "无报告"))

        with st.expander("⭐ 4. 评估与反馈", expanded=True):
            st.markdown(state.get("feedback", "无反馈"))

else:
    st.info("👆 输入主题后点击按钮开始")

# 页脚
st.markdown("---")
st.caption("基于 LangChain + DeepSeek + Tavily 构建")