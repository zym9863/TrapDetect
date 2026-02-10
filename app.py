import os
from pathlib import Path

import streamlit as st

from analyzer import analyze_text
from components.highlight import render_highlighted_text
from components.topology import render_topology
from models import AnalysisResult
from styles import PAGE_CSS

EXAMPLES_DIR = Path(__file__).parent / "examples"
TEXT_INPUT_KEY = "input_text"


def load_example(name: str) -> str:
    return (EXAMPLES_DIR / name).read_text(encoding="utf-8")


def get_risk_badge(level: str) -> str:
    labels = {"high": "HIGH RISK", "medium": "MED RISK", "low": "LOW RISK"}
    cn_labels = {"high": "高风险", "medium": "中风险", "low": "低风险"}
    label = labels.get(level, level)
    cn = cn_labels.get(level, "")
    return (
        f'<span class="risk-badge risk-{level}">'
        f'{label}<span style="margin-left:6px;font-size:0.7em;opacity:0.8;">{cn}</span>'
        f'</span>'
    )


def main() -> None:
    st.set_page_config(
        page_title="TrapDetect — 逻辑陷阱透视镜",
        page_icon="⬡",
        layout="wide",
    )
    st.markdown(PAGE_CSS, unsafe_allow_html=True)

    # ── 侧边栏 ──
    with st.sidebar:
        st.markdown(
            '<div style="padding:0.5rem 0 0.3rem;">'
            '<span style="font-family:JetBrains Mono,monospace;font-size:0.7rem;'
            'color:#00e5ff;letter-spacing:0.15em;text-transform:uppercase;">'
            'TrapDetect</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="scan-line" style="margin:0.6rem 0 1.2rem;"></div>',
            unsafe_allow_html=True,
        )

        # API Key 配置
        st.markdown(
            '<p style="font-family:JetBrains Mono,monospace;font-size:0.6rem;'
            'color:#3a4557;letter-spacing:0.12em;text-transform:uppercase;'
            'margin-bottom:0.3rem;">Configuration</p>',
            unsafe_allow_html=True,
        )
        env_key = os.environ.get("GEMINI_API_KEY", "")
        api_key = st.text_input(
            "Gemini API Key",
            value=env_key,
            type="password",
            help="优先读取环境变量 GEMINI_API_KEY，也可在此直接输入",
        )

        st.markdown(
            '<div class="scan-line" style="margin:1rem 0;"></div>',
            unsafe_allow_html=True,
        )

        # 示例文本
        st.markdown(
            '<p style="font-family:JetBrains Mono,monospace;font-size:0.6rem;'
            'color:#3a4557;letter-spacing:0.12em;text-transform:uppercase;'
            'margin-bottom:0.3rem;">Sample Data</p>',
            unsafe_allow_html=True,
        )
        examples = sorted(EXAMPLES_DIR.glob("*.txt")) if EXAMPLES_DIR.exists() else []
        example_names = [f.stem for f in examples]
        if example_names:
            selected_example = st.selectbox(
                "选择示例",
                options=["—"] + example_names,
                label_visibility="collapsed",
            )
            if selected_example != "—" and st.button("LOAD", use_container_width=True):
                st.session_state[TEXT_INPUT_KEY] = load_example(
                    f"{selected_example}.txt"
                )
                st.rerun()

        st.markdown(
            '<div class="scan-line" style="margin:1rem 0;"></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="padding-top:0.5rem;">'
            '<span style="font-family:JetBrains Mono,monospace;font-size:0.55rem;'
            'color:#2a3344;letter-spacing:0.1em;">v0.1.0 // Powered by Gemini</span>'
            '</div>',
            unsafe_allow_html=True,
        )

    # ── 主内容区：标题 ──
    st.markdown(
        '<div class="main-header">'
        '<h1 class="main-title">'
        '<span class="accent">⬡</span> 逻辑陷阱<span class="accent">透视镜</span>'
        '</h1>'
        '<p class="main-subtitle">'
        '上传或粘贴文本 — AI 深度扫描逻辑陷阱、风险条款与欺骗性表述'
        '</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── 输入区域 ──
    input_text = st.text_area(
        "待分析文本",
        value=st.session_state.get(TEXT_INPUT_KEY, ""),
        height=220,
        placeholder="在此粘贴待分析的文本 — 法律合同、营销文案、协议条款...",
        key=TEXT_INPUT_KEY,
    )

    uploaded = st.file_uploader(
        "或上传文本文件",
        type=["txt"],
        help="支持 .txt 格式",
    )
    if uploaded is not None:
        input_text = uploaded.read().decode("utf-8")
        st.session_state[TEXT_INPUT_KEY] = input_text

    # 分析按钮
    col1, col2 = st.columns([1, 5])
    with col1:
        analyze_btn = st.button(
            "SCAN", type="primary", use_container_width=True
        )

    if analyze_btn:
        if not api_key:
            st.error("请先配置 Gemini API Key（侧边栏或环境变量 GEMINI_API_KEY）")
            return
        if not input_text.strip():
            st.warning("请先输入或上传待分析的文本。")
            return

        with st.spinner("正在深度扫描文本中的逻辑陷阱..."):
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
        # 扫描线分隔
        st.markdown('<div class="scan-line"></div>', unsafe_allow_html=True)

        # 概览仪表盘
        trap_count = len(result.traps)
        relation_count = len(result.relations)

        st.markdown(
            f'<div class="overview-panel">'
            f'<div class="stat-card card-traps">'
            f'<div class="stat-label">Traps Detected · 检测陷阱</div>'
            f'<div class="stat-value val-traps">{trap_count}</div>'
            f'</div>'
            f'<div class="stat-card card-relations">'
            f'<div class="stat-label">Cross References · 跨段关联</div>'
            f'<div class="stat-value val-relations">{relation_count}</div>'
            f'</div>'
            f'<div class="stat-card card-risk">'
            f'<div class="stat-label">Overall Risk · 整体风险</div>'
            f'<div style="margin-top:0.3rem;">{get_risk_badge(result.overall_risk)}</div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # 总结
        st.markdown(
            f'<div class="summary-card">'
            f'<span class="summary-label">Analysis Summary · 分析总结</span>'
            f'{result.summary}'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Tab 切换
        tab_highlight, tab_topology = st.tabs(
            ["HIGHLIGHT · 智能高亮", "TOPOLOGY · 风险拓扑"]
        )

        with tab_highlight:
            render_highlighted_text(analyzed_text, result)

        with tab_topology:
            render_topology(result)

        # 详细分析列表
        if result.traps:
            st.markdown('<div class="scan-line"></div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="trap-detail-section">'
                '<h3>Trap Analysis · 陷阱详细解析</h3>'
                '</div>',
                unsafe_allow_html=True,
            )
            for trap in result.traps:
                severity_icon = {"high": "▲", "medium": "◆", "low": "●"}.get(
                    trap.severity, "○"
                )
                label = f'{severity_icon} {trap.trap_type} — "{trap.text[:40]}..."'
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
