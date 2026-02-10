import json
import re

from google import genai

from models import AnalysisResult
from prompts import build_analysis_prompt


def analyze_text(text: str, api_key: str) -> AnalysisResult:
    """调用 Gemini API 分析文本中的逻辑陷阱。"""
    client = genai.Client(api_key=api_key)

    prompt = build_analysis_prompt(text)
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )

    raw = response.text.strip()

    # 提取 JSON（可能被 markdown 代码块包裹）
    json_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw)
    if json_match:
        raw = json_match.group(1).strip()

    data = json.loads(raw)
    result = AnalysisResult.model_validate(data)

    # 校正索引：确保 text 字段与实际文本匹配
    for trap in result.traps:
        actual = text[trap.start_index : trap.end_index]
        if actual != trap.text:
            # 尝试在原文中查找精确匹配
            idx = text.find(trap.text)
            if idx != -1:
                trap.start_index = idx
                trap.end_index = idx + len(trap.text)

    return result
