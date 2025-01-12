import uuid
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
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables.config import RunnableConfig
from langgraph.store.base import BaseStore
from pymongo import MongoClient

load_dotenv()

class MongoDBStore(BaseStore):
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client.langgraph
        self.collection = self.db.langgraph

    def put(self, namespace, key, value):
        document = {"namespace": namespace, "key": key, "value": value}
        self.collection.insert_one(document)  # Synchronous MongoDB insert

    def get(self, namespace, key):
        document = self.collection.find_one({"namespace": namespace, "key": key})  # Synchronous MongoDB find
        return document["value"] if document else None

    def search(self, namespace, filter_dict):
        query = {"namespace": namespace, **filter_dict}
        cursor = self.collection.find(query)  # Find returns a cursor
        documents = list(cursor)  # Retrieve all results synchronously
        return [doc["value"] for doc in documents]

    def abatch(self, namespace, operations):
        """
        Implements batch operations synchronously.
        """
        for operation in operations:
            if operation["action"] == "put":
                self.put(namespace, operation["key"], operation["value"])
            elif operation["action"] == "delete":
                self.collection.delete_one({"namespace": namespace, "key": operation["key"]})

    def batch(self, namespace, operations):
        """
        Implements batch operations synchronously.
        """
        for operation in operations:
            if operation["action"] == "put":
                self.put(namespace, operation["key"], operation["value"])
            elif operation["action"] == "delete":
                self.collection.delete_one({"namespace": namespace, "key": operation["key"]})


llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

# Chatbot instruction
MODEL_SYSTEM_MESSAGE = """You are a helpful assistant with memory that provides information about the user.
If you have memory for this user, use it to personalize your responses.
Here is the memory (it may be empty): {memory}"""

CREATE_MEMORY_INSTRUCTION = """"You are collecting information about
the user to personalize your responses.

CURRENT USER INFORMATION:
{memory}

INSTRUCTIONS:
1. Review the chat history below carefully
2. Identify new information about the user, such as:
   - Personal details (name, location)
   - Preferences (likes, dislikes)
   - Interests and hobbies
   - Past experiences
   - Goals or future plans
3. Merge any new information with existing memory
4. Format the memory as a clear, bulleted list
5. If new information conflicts with existing memory, keep the most recent version

Remember: Only include factual information directly stated by the user. Do not make assumptions or inferences.

Based on the chat history below, please update the user information:"""

def call_model(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Load memory from the store and use it to personalize the chatbot's response."""
    user_id = config["configurable"]["user_id"]
    namespace = ("memory", user_id)
    key = "user_memory"
    existing_memory = store.get(namespace, key)  # Synchronous store.get

    if existing_memory:
        existing_memory_content = existing_memory.get('memory')
    else:
        existing_memory_content = "No existing memory found."
    print("existing_memory_content: " + existing_memory_content)
    system_msg = MODEL_SYSTEM_MESSAGE.format(memory=existing_memory_content)
    response = llm.invoke([SystemMessage(content=system_msg)] + state["messages"])

    return {"messages": response}


def write_memory(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Reflect on the chat history and save a memory to the store."""
    user_id = config["configurable"]["user_id"]
    namespace = ("memory", user_id)
    key = "user_memory"
    existing_memory = store.get(namespace, key)  # Synchronous store.get

    if existing_memory:
        existing_memory_content = existing_memory.get('memory')
    else:
        existing_memory_content = "No existing memory found."

    system_msg = CREATE_MEMORY_INSTRUCTION.format(memory=existing_memory_content)
    new_memory = llm.invoke([SystemMessage(content=system_msg)] + state['messages'])

    store.put(namespace, key, {"memory": new_memory.content})  # Synchronous store.put
    print("Updated Memory: " + new_memory.content)


# Define the graph
builder = StateGraph(MessagesState)
builder.add_node("call_model", call_model)
builder.add_node("write_memory", write_memory)
builder.add_edge(START, "call_model")
builder.add_edge("call_model", "write_memory")
builder.add_edge("write_memory", END)

# Store for long-term memory
across_thread_memory = MongoDBStore(uri=os.getenv("MONGODB_URI"))

# Checkpointer for short-term (within-thread) memory
within_thread_memory = MemorySaver()

# Compile the graph
graph = builder.compile(checkpointer=within_thread_memory, store=across_thread_memory)

app = FastAPI()

while True:
    user_input = input("Enter your query: ")
    config = {"configurable": {"thread_id": "1234", "user_id": "1"}}
    messages = graph.invoke({"messages": HumanMessage(content=user_input)}, config)
    for m in messages['messages']:
        m.pretty_print()

# @app.post("/chat")
# def chat(user_input: str):
#     config = {"configurable": {"thread_id": "123", "user_id": "1"}}
#     messages = graph.invoke({"messages": [HumanMessage(content=user_input)]}, config)  # Synchronous graph.invoke
#     return {"messages": [msg.content for msg in messages['messages']]}
