from langgraph.graph import END, StateGraph

from src.graph.nodes import (
    check_hallucination,
    generate_answer,
    retrieve_docs,
    rewrite_query,
)
from src.graph.state import AgentState


def build_graph():
    workflow = StateGraph(AgentState)

    # 1. Register nodes
    workflow.add_node("query_rewriter", rewrite_query)
    workflow.add_node("retriever", retrieve_docs)
    workflow.add_node("generator", generate_answer)
    workflow.add_node("hallucination_checker", check_hallucination)

    # 2. Linear transitions
    workflow.set_entry_point("query_rewriter")
    workflow.add_edge("query_rewriter", "retriever")
    workflow.add_edge("retriever", "generator")
    workflow.add_edge("generator", "hallucination_checker")

    # 3. Conditional routing
    def evaluate_route(state: AgentState):
        if state["hallucination_grade"] == "grounded" or state["retry_count"] >= 2:
            return END
        return "query_rewriter"

    workflow.add_conditional_edges(
        "hallucination_checker",
        evaluate_route,
        {
            END: END,
            "query_rewriter": "query_rewriter",
        },
    )

    return workflow.compile()


rag_graph = build_graph()