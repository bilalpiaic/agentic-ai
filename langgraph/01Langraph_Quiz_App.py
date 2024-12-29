
from typing_extensions import TypedDict # typ

from typing_extensions import TypedDict # type: ignore

class State(TypedDict):
    score: int
    user_input: str

def question_1(state):
    print("---Question 1---")
    print("What is the capital of France?")
    state['user_input'] = input("Your Answer: ")
    if state['user_input'].lower() == "paris":
        state['score'] += 1
    return state

def question_2(state):
    print("---Question 2---")
    print("What is 5 + 3?")
    state['user_input'] = input("Your Answer: ")
    if state['user_input'] == "8":
        state['score'] += 1
    else:
        print("Incorrect. The answer is 8.")
    return state


def question_3(state):
    print("---Question 3---")
    print("What is the color of the sky?")
    state['user_input'] = input("Your Answer: ")
    if state['user_input'].lower() in ["blue", "light blue"]:
        state['score'] += 1
    return state

from typing import Literal

def decide_next_question(state) -> Literal["question_2", "question_3"]:
    # Simple rule to alternate between questions for variety
    if state['score'] % 2 == 0:
        return "question_2"
    else:
        return "question_3"

from langgraph.graph import StateGraph, START, END

# Initialize the graph
builder = StateGraph(State)

# Add nodes
builder.add_node("question_1", question_1)
builder.add_node("question_2", question_2)
builder.add_node("question_3", question_3)

# Define edges
builder.add_edge(START, "question_1")  # Start with Question 1
builder.add_conditional_edges("question_1", decide_next_question)  # Decide next question
builder.add_edge("question_2", END)  # End after Question 2
builder.add_edge("question_3", END)  # End after Question 3

# Compile the graph
graph = builder.compile()

# Start the game
final_state = graph.invoke({"score": 0, "user_input": ""})

# Print the final score
print(f"Quiz Complete! Your final score is: {final_state['score']}")
