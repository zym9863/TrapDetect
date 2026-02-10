# TrapDetect

[中文](README.md) | [English](README-EN.md)

TrapDetect is a Streamlit + Gemini text analysis tool that automatically identifies logical traps and risky clauses in contracts, terms, and marketing copy, and visualizes them with highlights and a relationship topology graph.

**Key Features**
- Detects multiple trap types (hidden clauses, logical fallacies, vague wording, contradictory clauses, unequal terms, manipulative statements, liability traps, numeric traps)
- Highlights risky spans in the original text with explanations and severity levels
- Generates a relationship topology graph (contradiction/dependency/weakening/cooperation/progression)
- Supports pasting text or uploading `.txt` files
- Built-in sample text for quick tryout

**Tech Stack**
- UI/Rendering: Streamlit
- Model API: Gemini (`google-genai`)
- Data modeling: Pydantic
- Graph visualization: `streamlit-flow-component`

## Quick Start

**Requirements**
- Python 3.12+
- Gemini API Key (environment variable `GEMINI_API_KEY` or enter in the sidebar)

**Install Dependencies**
```bash
pip install -e .
```

This project uses `pyproject.toml` for dependency management. Use `uv` or `pip` as you prefer.

**Run the App**
```bash
streamlit run app.py
```

## Usage

1. Configure the Gemini API Key in the sidebar (recommended via `GEMINI_API_KEY`).
2. Paste text or upload a `.txt` file.
3. Click "Start Analysis".
4. Review:
   - Highlight view: trap spans + hover explanations
   - Topology graph: logical relationships between traps
   - Detail list: per-trap explanation and severity

## Output Schema (Model Response)

The model returns strict JSON. Field definitions are in `models.py`:
- `traps`: detected traps
- `relations`: relationships between traps
- `overall_risk`: overall risk level (high/medium/low)
- `summary`: summary and recommendations

## Project Structure

- `app.py`: Streamlit entry
- `analyzer.py`: Gemini call and parsing
- `prompts.py`: system prompts and analysis template
- `models.py`: Pydantic models
- `components/highlight.py`: highlight renderer
- `components/topology.py`: topology renderer
- `styles.py`: page and highlight styles
- `examples/`: sample texts

## Notes

- Model output is automated and for reference only; apply human judgment.
- Do not upload sensitive or protected data.
