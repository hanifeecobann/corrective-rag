from typing import Any, Dict

from graph.state import GraphState
from VectorDB import retriever


def retrieve(state: GraphState) -> Dict[str, Any]:
    print("--------Retrieve----------")

    question = state["question"]
    documents = retriever.invoke(question)

    return {"question": question, "documents": documents}