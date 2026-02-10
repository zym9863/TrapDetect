# 严重程度 -> 高亮背景色
SEVERITY_COLORS: dict[str, str] = {
    "high": "rgba(255, 75, 75, 0.35)",
    "medium": "rgba(255, 167, 38, 0.35)",
    "low": "rgba(255, 238, 88, 0.35)",
}

# 严重程度 -> 节点背景色（深色，用于拓扑图）
SEVERITY_NODE_COLORS: dict[str, str] = {
    "high": "#c62828",
    "medium": "#ef6c00",
    "low": "#f9a825",
}

# 文本高亮区域的 CSS 样式
HIGHLIGHT_CSS = """
<style>
.trap-text-container {
    font-size: 1rem;
    line-height: 1.8;
    padding: 1.2rem;
    border: 1px solid #ddd;
    border-radius: 8px;
    background: #fafafa;
    max-height: 600px;
    overflow-y: auto;
}

.trap-highlight {
    padding: 1px 2px;
    border-radius: 3px;
    cursor: help;
    position: relative;
    border-bottom: 2px solid transparent;
    transition: all 0.2s ease;
}

.trap-highlight:hover {
    filter: brightness(0.85);
    border-bottom-color: currentColor;
}

.trap-high {
    border-bottom-color: #e53935;
}

.trap-medium {
    border-bottom-color: #fb8c00;
}

.trap-low {
    border-bottom-color: #f9a825;
}
</style>
"""

# 全局页面样式
PAGE_CSS = """
<style>
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
}

[data-testid="stSidebar"] * {
    color: #e0e0e0 !important;
}

.risk-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 12px;
    font-weight: bold;
    font-size: 0.9em;
}

.risk-high {
    background: #ffcdd2;
    color: #b71c1c;
}

.risk-medium {
    background: #ffe0b2;
    color: #e65100;
}

.risk-low {
    background: #fff9c4;
    color: #f57f17;
}

.trap-detail-card {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 0.8rem;
    background: #fff;
}
</style>
"""
