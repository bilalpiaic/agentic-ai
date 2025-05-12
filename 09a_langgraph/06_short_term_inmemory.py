
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi import FastAPI
from langchain_core.messages import HumanMessage, SystemMessage


from dotenv import load_dotenv
import os
load_dotenv()

llm = ChatGoogleGenerativeAI( model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))


class MessagesState(TypedDict):
    messages: Annotated[list, add_messages]
    


def assistant(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_edge(START, "assistant")
builder.add_edge("assistant", END)
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

while True:
        user_input = input("Enter your query: ")
        config = {"configurable": {"thread_id": "1", "user_id": "1"}}
        messages = graph.invoke({"messages": HumanMessage(content=user_input)}, config)
        for m in messages['messages']:
            print(m.content)
            
app = FastAPI()

@app.get("/chat/{query}")
def get_content(query: str):
    print(query)
    try:
        config = {"configurable": {"thread_id": "1"}}
        result = graph.invoke({"messages": [("user", query)]}, config)
        return result
    except Exception as e:
        return {"output": str(e)}

# poetry run uvicorn 02Langraph_FastApi:app --reload

