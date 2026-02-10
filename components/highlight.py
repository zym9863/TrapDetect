import html

import streamlit as st

from models import AnalysisResult
from styles import HIGHLIGHT_CSS, SEVERITY_COLORS


def render_highlighted_text(text: str, result: AnalysisResult) -> None:
    """在原文中高亮显示识别到的陷阱。"""
    st.markdown(HIGHLIGHT_CSS, unsafe_allow_html=True)

    if not result.traps:
        st.markdown(
            f'<div class="trap-text-container">{html.escape(text)}</div>',
            unsafe_allow_html=True,
        )
        return

    # 按 start_index 排序，处理重叠
    sorted_traps = sorted(result.traps, key=lambda t: t.start_index)

    segments: list[str] = []
    last_end = 0

    for trap in sorted_traps:
        start = trap.start_index
        end = trap.end_index

        # 跳过无效或重叠的区间
        if start < last_end:
            start = last_end
        if start >= end or start >= len(text):
            continue

        # 添加陷阱之前的普通文本
        if start > last_end:
            segments.append(html.escape(text[last_end:start]))

        # 添加高亮的陷阱文本
        color = SEVERITY_COLORS.get(trap.severity, SEVERITY_COLORS["low"])
        trap_text = html.escape(text[start:end])
        tooltip = html.escape(f"[{trap.trap_type}] {trap.explanation}")
        segments.append(
            f'<span class="trap-highlight trap-{trap.severity}" '
            f'style="background-color: {color};" '
            f'title="{tooltip}" '
            f'data-trap-id="{trap.id}">'
            f"{trap_text}</span>"
        )
        last_end = end

    # 添加最后一段普通文本
    if last_end < len(text):
        segments.append(html.escape(text[last_end:]))

    rendered = "".join(segments).replace("\n", "<br>")
    st.markdown(
        f'<div class="trap-text-container">{rendered}</div>',
        unsafe_allow_html=True,
    )

    # 图例
    legend_items = [
        ("high", "High Risk · 高风险", "#ff1744"),
        ("medium", "Med Risk · 中风险", "#ff9100"),
        ("low", "Low Risk · 低风险", "#ffd600"),
    ]
    legend_html = '<div class="highlight-legend">'
    for level, label, color in legend_items:
        legend_html += (
            f'<div class="legend-item">'
            f'<span class="legend-dot" style="background:{color};color:{color};"></span>'
            f'{label}'
            f'</div>'
        )
    legend_html += '</div>'
    st.markdown(legend_html, unsafe_allow_html=True)
