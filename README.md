# TrapDetect

[中文](README.md) | [English](README-EN.md)


逻辑陷阱透视镜（TrapDetect）是一个基于 Streamlit + Gemini 的文本分析工具，用于自动识别合同/条款/营销文案中的逻辑陷阱与风险点，并以高亮与关系拓扑图的方式可视化展示。

**核心特性**
- 自动识别多类逻辑陷阱（隐藏条款、逻辑谬误、模糊用语、矛盾条款、不对等条款、诱导性表述、免责陷阱、数字陷阱）
- 高亮显示原文中的陷阱片段，并提供解释与严重程度
- 生成陷阱间关系拓扑图（矛盾/依赖/削弱/配合/递进）
- 支持粘贴文本或上传 `.txt` 文件
- 内置示例文本快速体验

**技术栈**
- 前端/展示：Streamlit
- 模型调用：Gemini (`google-genai`)
- 数据建模：Pydantic
- 关系图：`streamlit-flow-component`

## 快速开始

**环境要求**
- Python 3.12+
- Gemini API Key（环境变量 `GEMINI_API_KEY` 或在侧边栏输入）

**安装依赖**
```bash
pip install -e .
```

本项目使用 `pyproject.toml` 管理依赖，若你使用 `uv` 或 `pip` 可自行安装。

**启动应用**
```bash
streamlit run app.py
```

## 使用说明

1. 在侧边栏配置 Gemini API Key（推荐使用环境变量 `GEMINI_API_KEY`）。
2. 粘贴文本或上传 `.txt` 文件。
3. 点击“开始分析”。
4. 查看：
   - 高亮视图：陷阱片段 + 悬浮提示解释
   - 拓扑图：陷阱之间的逻辑关系
   - 详细列表：逐条陷阱的解释与风险等级

## 输出结构（模型返回）

模型返回严格的 JSON 结构，字段定义见 `models.py`：
- `traps`: 识别到的陷阱列表
- `relations`: 陷阱之间的关系列表
- `overall_risk`: 整体风险等级（high/medium/low）
- `summary`: 总结与建议

## 项目结构

- `app.py`: Streamlit 主入口
- `analyzer.py`: Gemini 调用与结果解析
- `prompts.py`: 系统提示词与分析模板
- `models.py`: Pydantic 数据模型
- `components/highlight.py`: 高亮渲染组件
- `components/topology.py`: 拓扑图渲染组件
- `styles.py`: 页面与高亮样式
- `examples/`: 示例文本

## 注意事项

- 模型输出为自动生成，仅供参考；请结合人工判断。
- 请勿上传敏感或受保护数据。
