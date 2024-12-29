from fastapi import FastAPI
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_text_splitters import CharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from dotenv import load_dotenv
from langgraph.graph import MessagesState
import os

load_dotenv()


llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

loader = TextLoader("./graph/data.txt")
documents = loader.load()

prompt = hub.pull("hwchase17/openai-tools-agent")

text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

db = FAISS.from_documents(texts, embeddings)
retriever = db.as_retriever()


info_retriever = create_retriever_tool(
    retriever,
    "hotel_information_sender",
    "Searches information about hotel from provided vector and return accurare as you can",
)

tools = [info_retriever]

llm_with_tools = llm.bind_tools(tools)

sys_msg = (
    "You are Alexandra Hotel's virtual assistant, trained to assist customers with any queries related to the hotel. "
    "Your primary responsibility is to provide accurate, helpful, and friendly responses. "
    "You have access to a specialized tool for retrieving detailed and up-to-date information about the hotel, "
    "such as amenities, room availability, pricing, dining options, events, and policies. Use this tool effectively to provide precise answers. "
    "If a query is beyond your scope or requires external actions (e.g., booking confirmation, cancellations), "
    "politely inform the user and guide them to contact the hotel's staff for further assistance. "
    "Maintain a professional yet approachable tone at all times."
)

#defining assistant it will call the llm_with_tools with the last 10 messages
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"][-10:])]}

#defining the nodes and edges of the graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

#here is the graph's memory
memory = MemorySaver()

#building up the graph
agent = builder.compile(checkpointer=memory)

app = FastAPI()

@app.get("/chat/{query}")
def get_content(query: str):
    print(query)
    try:
        config = {"configurable": {"thread_id": "1"}}
        result = agent.invoke({"messages": [("user", query)]}, config)
        return result
    except Exception as e:
        return {"output": str(e)}