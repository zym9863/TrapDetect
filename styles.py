# ──────────────────────────────────────────────
# TrapDetect 视觉系统 — "数字取证扫描仪" 主题
# ──────────────────────────────────────────────

# 严重程度 -> 高亮背景色
SEVERITY_COLORS: dict[str, str] = {
    "high": "rgba(255, 23, 68, 0.28)",
    "medium": "rgba(255, 145, 0, 0.25)",
    "low": "rgba(255, 214, 0, 0.22)",
}

# 严重程度 -> 节点背景色（用于拓扑图）
SEVERITY_NODE_COLORS: dict[str, str] = {
    "high": "#d50000",
    "medium": "#ef6c00",
    "low": "#f9a825",
}

# 严重程度 -> 描边光色
SEVERITY_GLOW: dict[str, str] = {
    "high": "#ff1744",
    "medium": "#ff9100",
    "low": "#ffd600",
}

# ── 文本高亮区域 CSS ──
HIGHLIGHT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

.trap-text-container {
    font-family: 'Noto Sans SC', sans-serif;
    font-size: 0.95rem;
    font-weight: 400;
    line-height: 2;
    padding: 1.8rem 2rem;
    border: 1px solid rgba(0, 229, 255, 0.12);
    border-radius: 4px;
    background: rgba(10, 12, 20, 0.85);
    color: #c8d6e5;
    max-height: 640px;
    overflow-y: auto;
    position: relative;
    letter-spacing: 0.01em;
    box-shadow:
        inset 0 1px 0 rgba(0, 229, 255, 0.06),
        0 4px 24px rgba(0, 0, 0, 0.4);
}

.trap-text-container::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00e5ff, transparent);
    animation: scanline-h 4s ease-in-out infinite;
}

@keyframes scanline-h {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 1; }
}

/* 滚动条 */
.trap-text-container::-webkit-scrollbar {
    width: 5px;
}
.trap-text-container::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.2);
}
.trap-text-container::-webkit-scrollbar-thumb {
    background: rgba(0, 229, 255, 0.3);
    border-radius: 4px;
}

.trap-highlight {
    padding: 2px 4px;
    border-radius: 2px;
    cursor: help;
    position: relative;
    border-bottom: 2px solid transparent;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    color: #f0f0f0;
    font-weight: 500;
}

.trap-highlight:hover {
    filter: brightness(1.4) saturate(1.3);
    border-bottom-color: currentColor;
    text-shadow: 0 0 8px currentColor;
}

.trap-high {
    border-bottom-color: #ff1744;
    text-shadow: 0 0 4px rgba(255, 23, 68, 0.3);
}

.trap-medium {
    border-bottom-color: #ff9100;
    text-shadow: 0 0 4px rgba(255, 145, 0, 0.2);
}

.trap-low {
    border-bottom-color: #ffd600;
    text-shadow: 0 0 4px rgba(255, 214, 0, 0.15);
}

/* ── 高亮图例 ── */
.highlight-legend {
    display: flex;
    gap: 1.5rem;
    padding: 0.8rem 0;
    margin-top: 0.6rem;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #8892a4;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.legend-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 6px currentColor;
}
</style>
"""

# ── 全局页面样式 ──
PAGE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

/* ═══════════════════════════════════════════
   全局基础
   ═══════════════════════════════════════════ */

.stApp {
    background: #06080e;
    color: #c8d6e5;
}

/* 微妙的网格纹理背景 */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0, 229, 255, 0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 229, 255, 0.015) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none;
    z-index: 0;
}

/* 全局字体 */
.stApp, .stApp p, .stApp span, .stApp div, .stApp li {
    font-family: 'Noto Sans SC', -apple-system, sans-serif !important;
}

h1, h2, h3, h4, h5, h6,
.stApp h1, .stApp h2, .stApp h3 {
    font-family: 'JetBrains Mono', 'Noto Sans SC', monospace !important;
    letter-spacing: -0.02em;
}

/* ═══════════════════════════════════════════
   侧边栏
   ═══════════════════════════════════════════ */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080b14 0%, #0d1117 50%, #0a0d15 100%) !important;
    border-right: 1px solid rgba(0, 229, 255, 0.08) !important;
}

[data-testid="stSidebar"]::after {
    content: '';
    position: absolute;
    top: 0; right: 0; bottom: 0;
    width: 1px;
    background: linear-gradient(180deg, transparent, rgba(0, 229, 255, 0.15), transparent);
    pointer-events: none;
}

[data-testid="stSidebar"] * {
    color: #8892a4 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #00e5ff !important;
    font-family: 'JetBrains Mono', monospace !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 0.85rem !important;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label {
    color: #5a6577 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

[data-testid="stSidebar"] .stCaption, [data-testid="stSidebar"] .stCaption p {
    color: #3a4557 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.08em;
}

/* 侧边栏输入框 */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(0, 229, 255, 0.04) !important;
    border: 1px solid rgba(0, 229, 255, 0.1) !important;
    border-radius: 4px !important;
    color: #c8d6e5 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
}

[data-testid="stSidebar"] input:focus {
    border-color: rgba(0, 229, 255, 0.3) !important;
    box-shadow: 0 0 0 2px rgba(0, 229, 255, 0.08) !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(0, 229, 255, 0.06) !important;
    margin: 1.2rem 0 !important;
}

[data-testid="stSidebar"] button {
    background: rgba(0, 229, 255, 0.08) !important;
    border: 1px solid rgba(0, 229, 255, 0.15) !important;
    color: #00e5ff !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    transition: all 0.2s ease !important;
}

[data-testid="stSidebar"] button:hover {
    background: rgba(0, 229, 255, 0.15) !important;
    border-color: rgba(0, 229, 255, 0.3) !important;
    box-shadow: 0 0 12px rgba(0, 229, 255, 0.1) !important;
}

/* ═══════════════════════════════════════════
   主标题区
   ═══════════════════════════════════════════ */

.main-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    position: relative;
}

.main-header::after {
    content: '';
    display: block;
    width: 120px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00e5ff, transparent);
    margin: 1.2rem auto 0;
}

.main-title {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 2rem !important;
    font-weight: 700;
    color: #e8edf3;
    letter-spacing: -0.02em;
    margin: 0;
    line-height: 1.2;
}

.main-title .accent {
    color: #00e5ff;
    text-shadow: 0 0 20px rgba(0, 229, 255, 0.3);
}

.main-subtitle {
    font-family: 'Noto Sans SC', sans-serif;
    font-size: 0.88rem;
    color: #5a6577;
    margin-top: 0.6rem;
    font-weight: 300;
    letter-spacing: 0.02em;
}

/* ═══════════════════════════════════════════
   输入区域
   ═══════════════════════════════════════════ */

.stTextArea textarea {
    background: rgba(10, 12, 20, 0.7) !important;
    border: 1px solid rgba(0, 229, 255, 0.1) !important;
    border-radius: 4px !important;
    color: #c8d6e5 !important;
    font-family: 'Noto Sans SC', sans-serif !important;
    font-size: 0.9rem !important;
    line-height: 1.8 !important;
    padding: 1rem 1.2rem !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}

.stTextArea textarea:focus {
    border-color: rgba(0, 229, 255, 0.3) !important;
    box-shadow: 0 0 0 2px rgba(0, 229, 255, 0.06), 0 0 20px rgba(0, 229, 255, 0.04) !important;
}

.stTextArea textarea::placeholder {
    color: #3a4557 !important;
    font-style: italic;
}

.stTextArea label, .stFileUploader label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #5a6577 !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* 文件上传 */
[data-testid="stFileUploader"] section {
    background: rgba(10, 12, 20, 0.5) !important;
    border: 1px dashed rgba(0, 229, 255, 0.12) !important;
    border-radius: 4px !important;
    padding: 1rem !important;
}

[data-testid="stFileUploader"] section:hover {
    border-color: rgba(0, 229, 255, 0.25) !important;
    background: rgba(0, 229, 255, 0.02) !important;
}

/* ═══════════════════════════════════════════
   按钮
   ═══════════════════════════════════════════ */

.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, rgba(0, 229, 255, 0.15), rgba(0, 229, 255, 0.08)) !important;
    border: 1px solid rgba(0, 229, 255, 0.3) !important;
    color: #00e5ff !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    border-radius: 4px !important;
    padding: 0.6rem 1.8rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative;
    overflow: hidden;
}

.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover {
    background: linear-gradient(135deg, rgba(0, 229, 255, 0.25), rgba(0, 229, 255, 0.12)) !important;
    border-color: rgba(0, 229, 255, 0.5) !important;
    box-shadow: 0 0 24px rgba(0, 229, 255, 0.15), 0 0 48px rgba(0, 229, 255, 0.05) !important;
    transform: translateY(-1px);
}

.stButton > button[kind="primary"]:active,
.stButton > button[data-testid="stBaseButton-primary"]:active {
    transform: translateY(0px);
}

/* ═══════════════════════════════════════════
   Metric 指标卡片
   ═══════════════════════════════════════════ */

[data-testid="stMetric"] {
    background: rgba(10, 14, 24, 0.7) !important;
    border: 1px solid rgba(0, 229, 255, 0.08) !important;
    border-radius: 4px !important;
    padding: 1.2rem 1.4rem !important;
    position: relative;
    overflow: hidden;
}

[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: #00e5ff;
    opacity: 0.6;
}

[data-testid="stMetric"] label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem !important;
    color: #5a6577 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    color: #e8edf3 !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
}

/* ═══════════════════════════════════════════
   风险徽章
   ═══════════════════════════════════════════ */

.risk-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 5px 14px;
    border-radius: 2px;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    font-size: 0.78em;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    position: relative;
}

.risk-high {
    background: rgba(255, 23, 68, 0.12);
    color: #ff1744;
    border: 1px solid rgba(255, 23, 68, 0.25);
    box-shadow: 0 0 12px rgba(255, 23, 68, 0.08);
    animation: pulse-red 3s ease-in-out infinite;
}

.risk-medium {
    background: rgba(255, 145, 0, 0.1);
    color: #ff9100;
    border: 1px solid rgba(255, 145, 0, 0.2);
    box-shadow: 0 0 12px rgba(255, 145, 0, 0.06);
}

.risk-low {
    background: rgba(255, 214, 0, 0.08);
    color: #ffd600;
    border: 1px solid rgba(255, 214, 0, 0.15);
}

@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 12px rgba(255, 23, 68, 0.08); }
    50% { box-shadow: 0 0 20px rgba(255, 23, 68, 0.2); }
}

/* ═══════════════════════════════════════════
   Tab 标签页
   ═══════════════════════════════════════════ */

.stTabs [data-baseweb="tab-list"] {
    gap: 0px;
    background: rgba(10, 12, 20, 0.5);
    border: 1px solid rgba(0, 229, 255, 0.06);
    border-radius: 4px;
    padding: 4px;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #5a6577 !important;
    border-radius: 3px !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #8892a4 !important;
    background: rgba(0, 229, 255, 0.04) !important;
}

.stTabs [aria-selected="true"] {
    color: #00e5ff !important;
    background: rgba(0, 229, 255, 0.08) !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background-color: #00e5ff !important;
    height: 2px !important;
}

.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* ═══════════════════════════════════════════
   Expander 展开面板
   ═══════════════════════════════════════════ */

.streamlit-expanderHeader {
    font-family: 'Noto Sans SC', sans-serif !important;
    font-size: 0.88rem !important;
    background: rgba(10, 14, 24, 0.6) !important;
    border: 1px solid rgba(0, 229, 255, 0.06) !important;
    border-radius: 4px !important;
    color: #c8d6e5 !important;
    transition: all 0.2s ease !important;
}

.streamlit-expanderHeader:hover {
    border-color: rgba(0, 229, 255, 0.15) !important;
    background: rgba(0, 229, 255, 0.03) !important;
}

[data-testid="stExpander"] details {
    border: 1px solid rgba(0, 229, 255, 0.06) !important;
    border-radius: 4px !important;
    background: rgba(10, 14, 24, 0.4) !important;
}

[data-testid="stExpander"] details[open] {
    border-color: rgba(0, 229, 255, 0.12) !important;
}

/* ═══════════════════════════════════════════
   Info / Warning / Error / Spinner
   ═══════════════════════════════════════════ */

[data-testid="stAlert"] {
    border-radius: 4px !important;
    font-family: 'Noto Sans SC', sans-serif !important;
}

.stAlert [data-testid="stAlertContentInfo"] {
    background: rgba(0, 229, 255, 0.06) !important;
    border-left: 3px solid #00e5ff !important;
    color: #a0b4c8 !important;
}

.stSpinner > div {
    border-top-color: #00e5ff !important;
}

/* ═══════════════════════════════════════════
   Divider
   ═══════════════════════════════════════════ */

hr, .stDivider {
    border-color: rgba(0, 229, 255, 0.06) !important;
}

/* ═══════════════════════════════════════════
   概览仪表盘
   ═══════════════════════════════════════════ */

.overview-panel {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 1rem;
    margin: 1.5rem 0;
}

.stat-card {
    background: rgba(10, 14, 24, 0.7);
    border: 1px solid rgba(0, 229, 255, 0.08);
    border-radius: 4px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.stat-card:hover {
    border-color: rgba(0, 229, 255, 0.18);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
}

.stat-card.card-traps::before { background: #ff1744; }
.stat-card.card-relations::before { background: #00e5ff; }
.stat-card.card-risk::before { background: #ff9100; }

.stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: #5a6577;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin-bottom: 0.5rem;
}

.stat-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #e8edf3;
    line-height: 1;
}

.stat-value.val-traps { color: #ff5252; }
.stat-value.val-relations { color: #00e5ff; }

/* ═══════════════════════════════════════════
   分析总结卡片
   ═══════════════════════════════════════════ */

.summary-card {
    background: rgba(0, 229, 255, 0.03);
    border: 1px solid rgba(0, 229, 255, 0.1);
    border-left: 3px solid #00e5ff;
    border-radius: 4px;
    padding: 1.2rem 1.6rem;
    margin: 1rem 0 1.5rem;
    font-family: 'Noto Sans SC', sans-serif;
    font-size: 0.9rem;
    color: #a0b4c8;
    line-height: 1.8;
}

.summary-card .summary-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: #00e5ff;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin-bottom: 0.6rem;
    display: block;
}

/* ═══════════════════════════════════════════
   扫描动画
   ═══════════════════════════════════════════ */

.scan-line {
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(0, 229, 255, 0.1) 20%,
        #00e5ff 50%,
        rgba(0, 229, 255, 0.1) 80%,
        transparent 100%
    );
    margin: 2rem 0;
    position: relative;
    overflow: hidden;
}

.scan-line::after {
    content: '';
    position: absolute;
    top: -2px; left: -100%;
    width: 60%;
    height: 6px;
    background: linear-gradient(90deg, transparent, rgba(0, 229, 255, 0.6), transparent);
    animation: scan-move 3s linear infinite;
}

@keyframes scan-move {
    0% { left: -60%; }
    100% { left: 100%; }
}

/* ═══════════════════════════════════════════
   陷阱详情卡片
   ═══════════════════════════════════════════ */

.trap-detail-section {
    margin-top: 1rem;
}

.trap-detail-section h3 {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #5a6577;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 1rem;
}

/* ═══════════════════════════════════════════
   Blockquote
   ═══════════════════════════════════════════ */

blockquote, .stMarkdown blockquote {
    border-left: 2px solid rgba(0, 229, 255, 0.2) !important;
    background: rgba(0, 229, 255, 0.02) !important;
    padding: 0.6rem 1rem !important;
    color: #8892a4 !important;
    font-style: italic;
}

/* ═══════════════════════════════════════════
   Code / inline code
   ═══════════════════════════════════════════ */

code {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8em !important;
    background: rgba(0, 229, 255, 0.06) !important;
    color: #00e5ff !important;
    padding: 2px 6px !important;
    border-radius: 2px !important;
    border: 1px solid rgba(0, 229, 255, 0.1) !important;
}

/* ═══════════════════════════════════════════
   拓扑图边框
   ═══════════════════════════════════════════ */

.topology-container {
    border: 1px solid rgba(0, 229, 255, 0.1);
    border-radius: 4px;
    overflow: hidden;
    position: relative;
    background: rgba(6, 8, 14, 0.9);
}

.topology-container::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        radial-gradient(rgba(0, 229, 255, 0.03) 1px, transparent 1px);
    background-size: 20px 20px;
    pointer-events: none;
    z-index: 0;
}

/* 关系图例 */
.relation-legend {
    display: flex;
    gap: 1.5rem;
    padding: 0.8rem 1rem;
    margin-top: 0.8rem;
    background: rgba(10, 14, 24, 0.5);
    border: 1px solid rgba(0, 229, 255, 0.06);
    border-radius: 4px;
}

.relation-legend-item {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #8892a4;
    letter-spacing: 0.04em;
}

.relation-legend-line {
    width: 16px;
    height: 2px;
    border-radius: 1px;
    display: inline-block;
}
</style>
"""
