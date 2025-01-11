import random
from typing_extensions import TypedDict, Literal

from langgraph.graph import StateGraph, START
from langgraph.types import Command

class State(TypedDict):
    query: str
    response: str


def handle_booking(state: State) -> Command[Literal["__end__"]]:
    # Simulate processing the booking request
    state["response"] = "Your booking request is being processed."
    return Command(update=state, goto="__end__")

def handle_cancellation(state: State) -> Command[Literal["__end__"]]:
    # Simulate processing the cancellation request
    state["response"] = "Your cancellation request is being processed."
    return Command(update=state, goto="__end__")

def handle_general_info(state: State) -> Command[Literal["__end__"]]:
    # Simulate providing general information
    state["response"] = "Here is some general information about our services."
    return Command(update=state, goto="__end__")


def route_query(state: State) -> Command[Literal["booking", "cancellation", "general_info"]]:
    if "book" in state["query"].lower():
        return Command(goto="booking")
    elif "cancel" in state["query"].lower():
        return Command(goto="cancellation")
    else:
        return Command(goto="general_info")


from langgraph.graph import StateGraph, START, END

graph = StateGraph(State)

# graph.add_node("route_query", route_query)
# graph.add_node("booking", handle_booking)
# graph.add_node("cancellation", handle_cancellation)
# graph.add_node("general_info", handle_general_info)

# # Define the edges
# graph.add_edge(START, "route_query")
# graph.add_conditional_edges("route_query", {
#     "booking": "booking",
#     "cancellation": "cancellation",
#     "general_info": "general_info"
# })
# graph.add_edge("booking", END)
# graph.add_edge("cancellation", END)
# graph.add_edge("general_info", END)


graph.add_node("route_query", route_query)
graph.add_node("booking", handle_booking)
graph.add_node("cancellation", handle_cancellation)
graph.add_node("general_info", handle_general_info)

# Define the edges
graph.add_edge(START, "route_query")

# Compile the graph
app = graph.compile()

while True:
    user_input = input("Enter your query: ")
    result = app.invoke({"query": user_input})
    print(result) 
