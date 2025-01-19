import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import Optional


# Define Onboarding Schema and LLM initialization
class OnboardingState(MessagesState):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]


class OnboardingSchema(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]


llm = ChatOpenAI(model="gpt-4o")

# System messages for onboarding assistant
sys_msg = """
You are an onboarding assistant for Signup. Your working flows are as follows:
- You will greet the user warmly.
- Then you will ask the user to Signup.
- Ask the user for username, email, and password.
- If the user provides the required information, populate the respective fields.
- You will continuously ask for missing information until onboarding is complete.
- After getting the complete information, say thanks to the user and inform them onboarding is complete.
"""

structured_sys_msg = """
You are collecting onboarding information from the user for Signup. The following information is required:
- username: The name of the user
- email: The email of the user
- password: The password of the user

The user may provide the information one by one, so you will be populating them as you are getting it.
Here are the current information fields from the user:
username: {username}
email: {email}
password: {password}
"""

# Define assistant function
def assistant(state: MessagesState):
    return {"messages": [llm.invoke([sys_msg] + state["messages"][-10:])]}


def populate_information(state: MessagesState):
    """Populate the user credentials into session state."""
    formatted_structured_msg = structured_sys_msg.format(
        username=st.session_state.get("username", ""),
        email=st.session_state.get("email", ""),
        password=st.session_state.get("password", ""),
    )
    response = llm.with_structured_output(OnboardingSchema).invoke(
        [formatted_structured_msg] + state["messages"]
    )

    # Update session state variables dynamically
    if response.username:
        st.session_state.username = response.username
    if response.email:
        st.session_state.email = response.email
    if response.password:
        st.session_state.password = response.password


# Define the StateGraph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("populate_information", populate_information)
builder.add_edge(START, "assistant")
builder.add_edge("populate_information", "populate_information")
builder.add_edge("populate_information", END)
memory = MemorySaver()
agent = builder.compile(checkpointer=memory)

st.set_page_config(page_title="Onboarding Assistant", page_icon=":robot:", layout="wide")

# Streamlit App Setup
st.title("Onboarding Assistant")
st.subheader("Interactive Signup")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "username" not in st.session_state:
    st.session_state.username = ""
if "email" not in st.session_state:
    st.session_state.email = ""
if "password" not in st.session_state:
    st.session_state.password = ""

# Layout columns
col1, col2 = st.columns(2)

# Chat Interface in the left column
with col1:
    st.subheader("Chat Interface")
    

    user_input = st.text_input("Enter your message:")
    if st.button("Send", key="send_button"):
        if user_input:
            # Add user message to session state
            human_message = HumanMessage(content=user_input)
            st.session_state.messages.append(human_message)

            # Invoke the agent and update messages
            response = agent.invoke({"messages": st.session_state.messages}, config = {"configurable": {"thread_id": "1234"}})
            st.session_state.messages = response["messages"]

            for message in reversed(st.session_state.messages):
                if isinstance(message, HumanMessage):
                    st.write(f"**You:** {message.content}")
                elif isinstance(message, AIMessage):
                    st.write(f"**Bot:** {message.content}")
            # Populate user credentials dynamically
            populate_information({"messages": st.session_state.messages})

# User Credentials Display in the right column
with col2:
    st.subheader("User Credentials Form")
    st.text_input("Username", value=st.session_state.username, disabled=True)
    st.text_input("Email", value=st.session_state.email, disabled=True)
    st.text_input("Password", value=st.session_state.password, disabled=True)
