
from typing_extensions import TypedDict # typ
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi import FastAPI


from dotenv import load_dotenv
import os
load_dotenv()

llm = ChatGoogleGenerativeAI( model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))


class MessagesState(TypedDict):
    output: str
    user_input: str 
    


def assistant(state: MessagesState):
    print(state["user_input"])
    return {"output": llm.invoke(state["user_input"])}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_edge(START, "assistant")
builder.add_edge("assistant", END)
graph = builder.compile()


app = FastAPI()

@app.get("/chat/{query}")
def get_content(query: str):
    print(query)
    try:
        result = graph.invoke({"user_input": query})
        return result
    except Exception as e:
        return {"output": str(e)}

# poetry run uvicorn 02Langraph_FastApi:app --reload

