import os
import sqlite3
from fastapi import FastAPI
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph, END
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables.config import RunnableConfig
from dotenv import load_dotenv

load_dotenv()

# Initialize Google Generative AI model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

# Chatbot instruction messages
MODEL_SYSTEM_MESSAGE = """You are a helpful assistant with memory that provides information about the user.
If you have memory for this user, use it to personalize your responses.
Here is the memory (it may be empty): {memory}"""

CREATE_MEMORY_INSTRUCTION = """You are collecting information about the user to personalize your responses.

CURRENT USER INFORMATION:
{memory}

INSTRUCTIONS:
1. Review the chat history below carefully.
2. Identify new information about the user, such as:
   - Personal details (name, location)
   - Preferences (likes, dislikes)
   - Interests and hobbies
   - Past experiences
   - Goals or future plans
3. Merge any new information with existing memory.
4. Format the memory as a clear, bulleted list.
5. If new information conflicts with existing memory, keep the most recent version.

Remember: Only include factual information directly stated by the user. Do not make assumptions or inferences.

Based on the chat history below, please update the user information:"""

def create_connection(db_file):
    """ Creates a database connection and table if it doesn't exist. """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS memories (
                          user_id TEXT PRIMARY KEY,
                          memory TEXT NOT NULL
                          );""")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    return conn

def get_connection():
    """ Gets the database connection (creating it if needed). """
    db_path = "memory.db"  # Database file in the current directory
    return create_connection(db_path)

def save_memory(user_id, memory):
    """ Saves the memory for a user in the database. """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO memories (user_id, memory) VALUES (?, ?)", (user_id, memory))
    conn.commit()
    conn.close()

def retrieve_memory(user_id):
    """ Retrieves the memory for a user from the database. """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT memory FROM memories WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def call_model(state: MessagesState, config: RunnableConfig):
    """ Load memory and use it in the chatbot's response. """
    user_id = config["configurable"]["user_id"]
    existing_memory = retrieve_memory(user_id)
    existing_memory_content = existing_memory if existing_memory else "No existing memory found."
    print("existing memory content: " + existing_memory_content)
    # Format the memory in the system prompt
    system_msg = MODEL_SYSTEM_MESSAGE.format(memory=existing_memory_content)
    # print("system_msg: " + system_msg)
    # Respond using memory as well as chat history
    response = llm.invoke([SystemMessage(content=system_msg)] + state["messages"])
    
    return {"messages": response}

def write_memory(state: MessagesState, config: RunnableConfig):
    """ Reflect on the chat history and save a memory to the store. """
    
    # Get user ID from config
    user_id = config["configurable"]["user_id"]
    
    existing_memory = retrieve_memory(user_id)
    existing_memory_content = existing_memory if existing_memory else "No existing memory found."
    
    # Format the memory in system prompt for updating
    system_msg = CREATE_MEMORY_INSTRUCTION.format(memory=existing_memory_content)
    
    new_memory_response = llm.invoke([SystemMessage(content=system_msg)] + state['messages'])
    
    # Save new memory to database; ensure content is valid string
    save_memory(user_id, new_memory_response.content)

# Define StateGraph for managing conversation flow
builder = StateGraph(MessagesState)
builder.add_node("call_model", call_model)
builder.add_node("write_memory", write_memory)
builder.add_edge(START, "call_model")
builder.add_edge("call_model", "write_memory")
builder.add_edge("write_memory", END)

# Checkpointer for short-term (within-thread) memory
within_thread_memory = MemorySaver()

# Compile graph with checkpointer for state management
graph = builder.compile(checkpointer=within_thread_memory)

app = FastAPI()

# Main loop for interaction (for testing purposes)
if __name__ == "__main__":
    # Ensure database file is created and accessible
    db_file_path = 'memory.db'
    
    if not os.path.exists(db_file_path):
        print(f"Database file '{db_file_path}' does not exist. It will be created.")
    
    while True:
        user_input = input("Enter your query: ")
        config = {"configurable": {"thread_id": "1", "user_id": "1"}}
        messages = graph.invoke({"messages": HumanMessage(content=user_input)}, config)
        for m in messages['messages']:
            print(m.content)  # Print responses from model

# Uncomment below to enable HTTP endpoint for chat interaction via FastAPI
# @app.get("/chat/{query}")
# def get_content(query: str):
#     try:
#         config = {"configurable": {"thread_id": "1", "user_id": "1"}}
#         result = graph.invoke({"messages": [HumanMessage(content=query)]}, config)
#         return result
#     except Exception as e:
#         return {"output": str(e)}
