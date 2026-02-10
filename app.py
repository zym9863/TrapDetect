import os
from pathlib import Path

import streamlit as st

from analyzer import analyze_text
from components.highlight import render_highlighted_text
from components.topology import render_topology
from models import AnalysisResult
from styles import PAGE_CSS

EXAMPLES_DIR = Path(__file__).parent / "examples"


def load_example(name: str) -> str:
    return (EXAMPLES_DIR / name).read_text(encoding="utf-8")


def get_risk_badge(level: str) -> str:
    labels = {"high": "高风险", "medium": "中风险", "low": "低风险"}
    label = labels.get(level, level)
    return f'<span class="risk-badge risk-{level}">{label}</span>'


def main() -> None:
    st.set_page_config(
        page_title="逻辑陷阱透视镜",
        page_icon="🔍",
        layout="wide",
    )
    st.markdown(PAGE_CSS, unsafe_allow_html=True)

    # ── 侧边栏 ──
    with st.sidebar:
        st.title("⚙️ 设置")

        # API Key 配置
        env_key = os.environ.get("GEMINI_API_KEY", "")
        api_key = st.text_input(
            "Gemini API Key",
            value=env_key,
            type="password",
            help="优先读取环境变量 GEMINI_API_KEY，也可在此直接输入",
        )

        st.divider()

        # 示例文本
        st.subheader("📄 示例文本")
        examples = sorted(EXAMPLES_DIR.glob("*.txt")) if EXAMPLES_DIR.exists() else []
        example_names = [f.stem for f in examples]
        if example_names:
            selected_example = st.selectbox(
                "选择示例",
                options=["（不使用示例）"] + example_names,
            )
            if selected_example != "（不使用示例）" and st.button("加载示例"):
                st.session_state["input_text"] = load_example(
                    f"{selected_example}.txt"
                )
                st.rerun()

        st.divider()
        st.caption("逻辑陷阱透视镜 v0.1.0")
        st.caption("Powered by Gemini")

    # ── 主内容区 ──
    st.title("🔍 逻辑陷阱透视镜")
    st.markdown("上传或粘贴文本（法律合同、营销文案、协议条款等），AI 将自动识别其中的逻辑陷阱和风险条款。")

    # 文本输入
    input_text = st.text_area(
        "待分析文本",
        value=st.session_state.get("input_text", ""),
        height=250,
        placeholder="在此粘贴待分析的文本...",
        key="text_input_area",
    )

    # 文件上传
    uploaded = st.file_uploader(
        "或上传文本文件",
        type=["txt"],
        help="支持 .txt 格式",
    )
    if uploaded is not None:
        input_text = uploaded.read().decode("utf-8")

    # 分析按钮
    col1, col2 = st.columns([1, 5])
    with col1:
        analyze_btn = st.button("🚀 开始分析", type="primary", use_container_width=True)

    if analyze_btn:
        if not api_key:
            st.error("请先配置 Gemini API Key（侧边栏或环境变量 GEMINI_API_KEY）")
            return
        if not input_text.strip():
            st.warning("请先输入或上传待分析的文本。")
            return

        with st.spinner("AI 正在深度分析文本中的逻辑陷阱..."):
            try:
                result = analyze_text(input_text, api_key)
                st.session_state["analysis_result"] = result
                st.session_state["analyzed_text"] = input_text
            except Exception as e:
                st.error(f"分析失败：{e}")
                return

    # ── 展示分析结果 ──
    result: AnalysisResult | None = st.session_state.get("analysis_result")
    analyzed_text: str | None = st.session_state.get("analyzed_text")

    if result and analyzed_text:
        st.divider()

        # 概览
        trap_count = len(result.traps)
        relation_count = len(result.relations)

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("检测到的陷阱", f"{trap_count} 个")
        col_b.metric("跨段落关联", f"{relation_count} 条")
        col_c.markdown(
            f"**整体风险等级：** {get_risk_badge(result.overall_risk)}",
            unsafe_allow_html=True,
        )

        # 总结
        st.info(f"📋 **分析总结：** {result.summary}")

        # Tab 切换
        tab_highlight, tab_topology = st.tabs(["📝 智能高亮", "🕸️ 风险拓扑图"])

        with tab_highlight:
            render_highlighted_text(analyzed_text, result)

        with tab_topology:
            render_topology(result)

        # 详细分析列表
        if result.traps:
            st.divider()
            st.subheader("📊 陷阱详细解析")
            for trap in result.traps:
                severity_emoji = {"high": "🔴", "medium": "🟠", "low": "🟡"}.get(
                    trap.severity, "⚪"
                )
                label = f'{severity_emoji} {trap.trap_type} — \u201c{trap.text[:40]}...\u201d'
                with st.expander(label):
                    st.markdown(f"**原文片段：**\n> {trap.text}")
                    st.markdown(f"**类型：** {trap.trap_type}")
                    st.markdown(
                        f"**严重程度：** {get_risk_badge(trap.severity)}",
                        unsafe_allow_html=True,
                    )
                    st.markdown(f"**所在段落：** 第 {trap.paragraph_index + 1} 段")
                    st.markdown(f"**详细解析：**\n\n{trap.explanation}")

                    # 显示关联关系
                    related = [
                        r
                        for r in result.relations
                        if r.source_id == trap.id or r.target_id == trap.id
                    ]
                    if related:
                        st.markdown("**关联关系：**")
                        for rel in related:
                            other_id = (
                                rel.target_id
                                if rel.source_id == trap.id
                                else rel.source_id
                            )
                            direction = (
                                "→" if rel.source_id == trap.id else "←"
                            )
                            st.markdown(
                                f"- {direction} `{other_id}` [{rel.relation_type}] {rel.description}"
                            )


if __name__ == "__main__":
    main()
