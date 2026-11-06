from typing import Any, Dict
from graph.chains.retrieval_grader import retrival_grader
from graph.state import GraphState


def grade_documents(state: GraphState) -> Dict[str, Any]:
    print("----------Check document relevant to question------------")

    question = state["question"]
    documents = state["documents"]

    filtered_docs = []
    web_search = False

    for d in documents:
        score = retrival_grader.invoke({
            "question": question,
            "document": d.page_content
        })

        grade = score.binary_score

        if grade.lower() == "yes":
            print("---------Grade: Document Relevant-----------")
            filtered_docs.append(d)
        else:
            print("---------Grade: Document Not Relevant-----------")
            web_search = True

    return {
        "question": question,
        "documents": filtered_docs,
        "web_search": web_search
    }