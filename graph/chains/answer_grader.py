from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


class GradeAnswer(BaseModel):
    binary_score: str = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )

llm = ChatAnthropic(model="claude-sonnet-4-6")
structured_llm_grader = llm.with_structured_output(GradeAnswer, method="json_schema")

system_prompt = """You are a grader assessing whether an answer addresses / resolves a question.
Give a binary score 'yes' or 'no'. 'yes' means that the answer resolves the question."""

answer_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "User question: \n\n {question} \n\n LLM generation: {generation}")
])

answer_grader = answer_prompt | structured_llm_grader