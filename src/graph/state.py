from typing import List, TypedDict


class AgentState(TypedDict):
    question: str
    rewritten_query: str
    documents: List[str]
    generation: str
    hallucination_grade: str  # "grounded" or "hallucinated"
    retry_count: int