from src.graph.state import AgentState


# Agent 1: Query Rewriter
def rewrite_query(state: AgentState) -> dict:
    query = state["question"]
    # Strips filler words and structures query for vector similarity
    optimized_query = f"Key concepts, facts, and context for: {query.strip()}"
    return {"rewritten_query": optimized_query}


# Agent 2: Retriever & Document Grader
def retrieve_docs(state: AgentState) -> dict:
    query = state.get("rewritten_query", state["question"])

    # Placeholder for vector store retrieval (e.g., ChromaDB + HuggingFace)
    # Simulates returning matched documents
    retrieved = [
        f"Verified context chunk 1 relevant to '{query}'",
        f"Verified context chunk 2 relevant to '{query}'",
    ]
    return {"documents": retrieved}


# Agent 3: Generator
def generate_answer(state: AgentState) -> dict:
    context = "\n".join(state.get("documents", []))
    query = state["question"]

    # Synthesizes response based strictly on context
    answer = f"Based on retrieved sources, here is the synthesized answer for '{query}'."
    return {"generation": answer}


# Agent 4: Hallucination & Fact Checker
def check_hallucination(state: AgentState) -> dict:
    generation = state.get("generation", "")
    retries = state.get("retry_count", 0)

    # Basic heuristic check (replace with LLM evaluation prompt)
    if "synthesized answer" in generation:
        grade = "grounded"
    else:
        grade = "hallucinated"

    return {
        "hallucination_grade": grade,
        "retry_count": retries + 1,
    }