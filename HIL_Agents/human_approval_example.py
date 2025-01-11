from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import os
from langgraph.types import Command, interrupt

post_ideas = {"yesterday": "on langchain", "today": "on langgraph", "tommorow": "on langgsmith"}

class State(TypedDict):
    linkedin_post: str
    is_posted: bool
    topic: str

def create_linkedin_post(state) -> Command[Literal["__end__", "human_approval"]]:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))
    linkedin_post = llm.invoke(f"""You are a skilled LinkedIn post writer. write a post on the topic of {state["topic"]}""")
    return Command(update={"linkedin_post": linkedin_post}, goto="human_approval")

def post_to_linkedin(state) -> Command[Literal["__end__"]]:
    linkedin_post = state["linkedin_post"]
    print(f"Posting to LinkedIn...")
    print("Posted")
    return Command(update = {"is_posted": True}, goto="__end__")

def human_approval(state) -> Command[Literal["__end__", "post_to_linkedin"]]:
    print("---human_feedback---")

    is_approved = interrupt({'task': "Check the post..", 'post': state['linkedin_post']})

    print("\n\n[RESUME AFTER INTERRUPT:]\n\n", is_approved)

    if is_approved == "yes":
        return Command(goto="post_to_linkedin")
    else:
        return Command(goto="__end__")



builder = StateGraph(State)
builder.add_node("create_linkedin_post", create_linkedin_post)
builder.add_node("human_approval", human_approval)
builder.add_node("post_to_linkedin", post_to_linkedin)

builder.add_edge(START, "create_linkedin_post")

# Set up memory
memory = MemorySaver()

# Add
graph = builder.compile(checkpointer=memory)

def is_agent_interrupted(agent, config):
    state_snapshot = agent.get_state(config)
    for task in state_snapshot.tasks:
        if task.interrupts:
            return True
    return False

while True:
    config = {"configurable": {"thread_id": "2"}}
    user_input = input("Enter the topic: ")
    result = graph.invoke({"topic": user_input}, config)
    print('result:', result['linkedin_post'].content)
    is_interrupted = is_agent_interrupted(graph, config)
    if is_interrupted:
        print("Agent is interrupted so getting human feedback...")
        human_feedback = input("You approval is required. Read the post and Say yes to approve or no to disapprove: ")
        graph.invoke(Command(resume=human_feedback), config=config)