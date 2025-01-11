from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from langgraph.types import Command, interrupt


class State(TypedDict):
    input: str
    user_feedback: str


def step_1(state):
    print("---Step 1---")
    pass


def human_feedback(state):
    print("---human_feedback---")

    feedback = interrupt({"Please provide feedback:": "WAITING to Start"})

    print("\n\n[GOT BACK FROM HUMAN AFTER INTERRUPT:]\n\n", feedback)
    return {"user_feedback": feedback}


def step_3(state):
    print("---Step 3---")
    pass


builder = StateGraph(State)
builder.add_node("step_1", step_1)
builder.add_node("human_feedback", human_feedback)
builder.add_node("step_3", step_3)

builder.add_edge(START, "step_1")
builder.add_edge("step_1", "human_feedback")
builder.add_edge("human_feedback", "step_3")
builder.add_edge("step_3", END)

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
        second_result = graph.invoke(Command(resume="human_feedback"), config=config)
        print("second_result", second_result) 