from typing_extensions import TypedDict
from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from langgraph.types import Command, interrupt


class State(TypedDict):
    input: str

def human_approval(state) -> Command[Literal["__end__", "call_agent"]]:
    print("---human_feedback---")

    is_approved = interrupt("Is this correct?")

    print("\n\n[RESUME AFTER INTERRUPT:]\n\n", is_approved)

    if is_approved == "yes":
        return Command(goto="call_agent")
    else:
        return Command(goto="__end__")


def call_agent(state):
    print("---call_agent 3---")
    pass


builder = StateGraph(State)
builder.add_node("human_approval", human_approval)
builder.add_node("call_agent", call_agent)

builder.add_edge(START, "human_approval")

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
    user_input = input("Enter your query: ")
    graph.invoke({"input": user_input}, config)
    is_interrupted = is_agent_interrupted(graph, config)
    if is_interrupted:
        print("Agent is interrupted so getting human feedback...")
        human_feedback = input("Human Please provide feedback: ")
        second_result = graph.invoke(Command(resume=human_feedback), config=config)
        print("second_result", second_result) 