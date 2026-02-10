import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowEdge, StreamlitFlowNode
from streamlit_flow.layouts import ForceLayout
from streamlit_flow.state import StreamlitFlowState

from models import AnalysisResult
from styles import SEVERITY_COLORS, SEVERITY_NODE_COLORS

# 关系类型对应的边样式
RELATION_EDGE_STYLES: dict[str, dict] = {
    "矛盾": {"stroke": "#ff1744", "strokeWidth": 2},
    "依赖": {"stroke": "#00e5ff", "strokeWidth": 2},
    "削弱": {"stroke": "#ff9100", "strokeWidth": 2},
    "配合": {"stroke": "#00e676", "strokeWidth": 2},
    "递进": {"stroke": "#d500f9", "strokeWidth": 2},
}


def render_topology(result: AnalysisResult) -> None:
    """渲染陷阱之间的交互式关系拓扑图。"""
    if not result.traps:
        st.info("未检测到陷阱，无法生成拓扑图。")
        return

    # 构建节点
    nodes: list[StreamlitFlowNode] = []
    for i, trap in enumerate(result.traps):
        node_color = SEVERITY_NODE_COLORS.get(
            trap.severity, SEVERITY_NODE_COLORS["low"]
        )
        label = f"**{trap.trap_type}**\n{trap.text[:20]}..."
        nodes.append(
            StreamlitFlowNode(
                id=trap.id,
                pos=(i * 200, 0),
                data={"content": label},
                node_type="default",
                source_position="right",
                target_position="left",
                style={
                    "background": f"linear-gradient(135deg, {node_color}, {node_color}dd)",
                    "color": "#fff",
                    "border": f"1px solid {SEVERITY_COLORS.get(trap.severity, 'rgba(0,229,255,0.2)')}",
                    "borderRadius": "4px",
                    "padding": "10px 12px",
                    "fontSize": "11px",
                    "fontFamily": "'Noto Sans SC', sans-serif",
                    "width": "160px",
                    "boxShadow": f"0 4px 16px {node_color}44",
                    "backdropFilter": "blur(8px)",
                },
            )
        )

    # 构建边
    edges: list[StreamlitFlowEdge] = []
    for rel in result.relations:
        edge_style = RELATION_EDGE_STYLES.get(
            rel.relation_type, {"stroke": "#5a6577", "strokeWidth": 1}
        )
        edges.append(
            StreamlitFlowEdge(
                id=f"{rel.source_id}-{rel.target_id}",
                source=rel.source_id,
                target=rel.target_id,
                animated=True,
                label=rel.relation_type,
                label_show_bg=True,
                label_bg_style={
                    "fill": "#0a0e18",
                    "fillOpacity": "0.9",
                },
                style=edge_style,
                marker_end={"type": "arrowclosed"},
            )
        )

    if not edges:
        st.info("各陷阱之间未发现跨段落的逻辑关联。")
        if len(nodes) == 1:
            st.markdown(
                f"**检测到 1 个独立陷阱：** {result.traps[0].trap_type} — {result.traps[0].text[:50]}"
            )
            return

    state = StreamlitFlowState(nodes=nodes, edges=edges)

    selected = streamlit_flow(
        key="trap_topology",
        state=state,
        layout=ForceLayout(),
        height=500,
        fit_view=True,
        show_controls=True,
        show_minimap=True,
        pan_on_drag=True,
        allow_zoom=True,
        min_zoom=0.3,
        hide_watermark=True,
        get_node_on_click=True,
        get_edge_on_click=True,
        style={
            "border": "1px solid rgba(0, 229, 255, 0.1)",
            "borderRadius": "4px",
            "background": "#06080e",
        },
    )

    # 点击节点显示详情
    if selected and selected.selected_id:
        selected_id = selected.selected_id
        for trap in result.traps:
            if trap.id == selected_id:
                st.markdown(f"### {trap.trap_type}")
                st.markdown(f"> {trap.text}")
                st.markdown(f"**严重程度：** {trap.severity}")
                st.markdown(f"**解析：** {trap.explanation}")
                break
        else:
            for rel in result.relations:
                edge_id = f"{rel.source_id}-{rel.target_id}"
                if edge_id == selected_id:
                    st.markdown(f"### 关系：{rel.relation_type}")
                    st.markdown(f"**描述：** {rel.description}")
                    break

    # 关系图例
    if edges:
        legend_parts = []
        for rtype, style in RELATION_EDGE_STYLES.items():
            legend_parts.append(
                f'<div class="relation-legend-item">'
                f'<span class="relation-legend-line" style="background:{style["stroke"]};"></span>'
                f'{rtype}'
                f'</div>'
            )
        st.markdown(
            f'<div class="relation-legend">{"".join(legend_parts)}</div>',
            unsafe_allow_html=True,
        )
