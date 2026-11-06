from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("human",
     "You are an assistant for question-answering tasks. "
     "Use the following pieces of retrieved context to answer the question. "
     "If you don't know the answer, just say that you don't know. "
     "Use three sentences maximum and keep the answer concise.\n"
     "Question: {question}\n"
     "Context: {context}\n"
     "Answer:"),
])

generation_chain = prompt | llm | StrOutputParser()