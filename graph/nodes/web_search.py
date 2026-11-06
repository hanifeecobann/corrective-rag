from typing import Any, Dict

from langchain_core.documents import Document
from langchain_community.tools.tavily_search import TavilySearchResults

from graph.state import GraphState

web_search_tool = TavilySearchResults(max_results=3)


def web_search(state: GraphState) -> Dict[str, Any]:
    print("-----------Web Search-----------")
    question = state["question"]
    documents = state.get("documents") or []   # yoksa boş liste

    tavily_results = web_search_tool.invoke({"query": question})
    joined_results = "\n".join([r["content"] for r in tavily_results])
    documents.append(Document(page_content=joined_results))

    return {"documents": documents, "question": question}