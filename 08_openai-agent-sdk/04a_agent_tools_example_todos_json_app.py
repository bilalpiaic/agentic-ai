import json
from openai import AsyncOpenAI
from regex import E
from agents import Agent, OpenAIChatCompletionsModel, Runner,function_tool
import os
from dotenv import load_dotenv


load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


@function_tool
def list_todos():
    """List all todos from the todos.json file."""
    try:
        print("Listing todos...")
        with open("08_openai-agent-sdk/todos.json", "r") as file:
            data = json.load(file)  # Use json.load to read directly from file
        return data
    except Exception as e:
        print(f"Error: {e}")
        raise FileNotFoundError("The file todos.json was not found.")
    
import json
from typing import Dict, Any
from datetime import datetime

@function_tool
def add_todo(title: str, description: str = "", due_date: str = "") -> Dict[str, Any]:
    """Add a new todo to the todos.json file.
    
    Args:
        title: The title of the todo.
        description: Optional description of the todo.
        due_date: Optional due date in YYYY-MM-DD format.
    
    Returns:
        The newly created todo item.
    """
    try:
        # Read existing todos
        try:
            with open("08_openai-agent-sdk/todos.json", "r") as file:
                todos = json.load(file)
        except FileNotFoundError:
            todos = []  # If file doesn't exist, start with an empty list
        except json.JSONDecodeError:
            raise ValueError("Error decoding todos.json. Ensure it contains valid JSON.")

        # Create new todo
        new_todo = {
            "id": len(todos) + 1,  # Simple incremental ID
            "title": title,
            "description": description,
            "completed": False,  # Default to not completed
            "dueDate": due_date if due_date else datetime.now().strftime("%Y-%m-%d")
        }

        # Append and save
        todos.append(new_todo)
        with open("08_openai-agent-sdk/todos.json", "w") as file:
            json.dump(todos, file, indent=2)

        return new_todo

    except Exception as e:
        raise Exception(f"Failed to add todo: {str(e)}")

agent = Agent(
    name="Todos Assistant",
    instructions="You are an expert of todos. You can add, list, and complete todos.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[list_todos, add_todo],
)

query = input("Enter the query: ")

result = Runner.run_sync(
    agent,
    query,
)

print(result.final_output)