from typing import Any, Literal, Union
import requests
from langchain_core.tools import tool
from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage, AnyMessage
from pydantic import BaseModel
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from langgraph.graph import MessagesState
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    trim_messages,
)
import requests
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START
from typing import Optional, Annotated
from langgraph.prebuilt import InjectedState


class OnboardingState(MessagesState):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]

class OnboardingSchema(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]

llm = ChatOpenAI(model="gpt-4o")

user_data = [{"username": "user1", "email": "zainatteeq@gmail.com", "password": "123456"},
             {"username": "user2", "email": "abc@gmail.com", "password": "123456"}]
#define the system message to the llm
sys_msg = """
You are a onboarding assistant for Signup. Your working flows is as follows:
- You will greet the user warmly
- Then you will ask the user to Signup
- Ask the user for username, email and password
- If the user provide the required information. Call the `populate_information` tool to populate the information.
- You will be continuously asking the user the required information until you got the complete information
- After getting the complete information Say Thanks to the user and tell him that his onboarding is complete.

Guidelines:
-Don't ask other questions irrelevant to you.
-Only call the populate_information tool, If the user provide required infromation which you have to populate.
"""

structured_sys_msg = """
You are collecting onboarding information from the user for Signup. The following information is required:
-username: The name of the user
-email: The email of the user
-password: The password of the user

The user may provide the information one by one so you will be populating them as you are getting it. 
Here are the current information fields got from the user:
username: {username}
email: {email}
password: {password}
"""


#defining assistant it will call the llm_with_tools with the last 10 messages
def assistant(state: MessagesState):
    return {"messages": [llm.invoke([sys_msg] + state["messages"][-10:])]}

def populate_information(state: MessagesState):
  """Populate the required user credentials on the Signup page: username, email and password"""
  #have to call trustcall or structured output to the messages to extract the relevant information from it.
  messages = state['messages']
  formatted_structred_sys_msg = structured_sys_msg.format(username = state['username'], email = state['email'], password = state['password'])
  response = llm.with_structured_output(OnboardingSchema).invoke([formatted_structred_sys_msg] + messages)
  return {"username": state['username'], 'email': state['email'], 'password': state['password']}

#defining the nodes and edges of the graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("populate_information", populate_information)

builder.add_edge(START, "assistant")
builder.add_edge("populate_information", "populate_information")
builder.add_edge("populate_information", END)

#here is the graph's memory
memory = MemorySaver()

#building up the graph
agent = builder.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "1234"}}
while True:
  inp = input("Enter query:")
  messages = [HumanMessage(content=f"{inp}")]
  messages = agent.invoke({"messages": messages}, config)
  for m in messages['messages']:
    m.pretty_print()