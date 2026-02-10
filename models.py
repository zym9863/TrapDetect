from pydantic import BaseModel


class Trap(BaseModel):
    id: str
    text: str
    start_index: int
    end_index: int
    trap_type: str
    severity: str  # high / medium / low
    explanation: str
    paragraph_index: int


class TrapRelation(BaseModel):
    source_id: str
    target_id: str
    relation_type: str
    description: str


class AnalysisResult(BaseModel):
    traps: list[Trap]
    relations: list[TrapRelation]
    overall_risk: str  # high / medium / low
    summary: str
