from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from VectorDB import retriever
from graph.chains.router import structured_llm_router
load_dotenv()
llm=ChatAnthropic(model="claude-sonnet-4-6", temperature=0)

class GradeDocuments(BaseModel):
    binary_score: str = Field(
        description="Documents are relevant to the question,'yes' or 'no'"
    )

structured_llm_grader = llm.with_structured_output(GradeDocuments, method="json_schema")


system_prompt="""
You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts.
Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts.
"""
grade_prompt=ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human","Retrieved document: {document} User question: {question}" )

    ]
)
retrival_grader=grade_prompt | structured_llm_grader




if __name__ == "__main__":
    user_question="what is prompt engineering?"
    docs = retriever.get_relevant_documents("what is ptompt enginering?")
    retrieved_document= docs[0].page_content
    print(retrival_grader.invoke(
       {"question": user_question,"document": retrieved_document}
    ))
