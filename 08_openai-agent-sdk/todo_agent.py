from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, Tool
import os
from dotenv import load_dotenv
import sqlite3
from datetime import datetime
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = AsyncOpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)

# Database setup
def init_db():
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Tool implementations
def add_todo(title: str, description: str = "") -> Dict[str, Any]:
    """Add a new todo item to the database."""
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute(
        'INSERT INTO todos (title, description) VALUES (?, ?)',
        (title, description)
    )
    conn.commit()
    todo_id = c.lastrowid
    conn.close()
    return {"id": todo_id, "title": title, "description": description, "status": "pending"}

def list_todos(status: str = None) -> List[Dict[str, Any]]:
    """List all todos, optionally filtered by status."""
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    
    if status:
        c.execute('SELECT * FROM todos WHERE status = ?', (status,))
    else:
        c.execute('SELECT * FROM todos')
    
    todos = []
    for row in c.fetchall():
        todos.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": row[3],
            "created_at": row[4],
            "completed_at": row[5]
        })
    conn.close()
    return todos

def complete_todo(todo_id: int) -> Dict[str, Any]:
    """Mark a todo as completed."""
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute(
        'UPDATE todos SET status = ?, completed_at = ? WHERE id = ?',
        ('completed', now, todo_id)
    )
    conn.commit()
    
    c.execute('SELECT * FROM todos WHERE id = ?', (todo_id,))
    todo = c.fetchone()
    conn.close()
    
    if todo:
        return {
            "id": todo[0],
            "title": todo[1],
            "description": todo[2],
            "status": "completed",
            "created_at": todo[4],
            "completed_at": now
        }
    return None

def delete_todo(todo_id: int) -> bool:
    """Delete a todo item."""
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    success = c.rowcount > 0
    conn.close()
    return success

# Initialize database
init_db()

# Create tools
tools = [
    Tool(
        name="add_todo",
        description="Add a new todo item with a title and optional description",
        function=add_todo,
        parameters={
            "title": {"type": "string", "description": "The title of the todo item"},
            "description": {"type": "string", "description": "Optional description of the todo item"}
        }
    ),
    Tool(
        name="list_todos",
        description="List all todos, optionally filtered by status (pending/completed)",
        function=list_todos,
        parameters={
            "status": {"type": "string", "description": "Optional status filter (pending/completed)"}
        }
    ),
    Tool(
        name="complete_todo",
        description="Mark a todo item as completed",
        function=complete_todo,
        parameters={
            "todo_id": {"type": "integer", "description": "The ID of the todo item to complete"}
        }
    ),
    Tool(
        name="delete_todo",
        description="Delete a todo item",
        function=delete_todo,
        parameters={
            "todo_id": {"type": "integer", "description": "The ID of the todo item to delete"}
        }
    )
]

# Create the agent
agent = Agent(
    name="TodoAssistant",
    instructions="""You are a helpful Todo management assistant. You can:
    1. Add new todo items
    2. List all todos or filter by status
    3. Mark todos as completed
    4. Delete todos
    Always be clear and concise in your responses. When listing todos, format them nicely.""",
    model=OpenAIChatCompletionsModel(
        model="gpt-3.5-turbo",
        openai_client=client
    ),
    tools=tools
)

def main():
    print("Welcome to the Todo Assistant!")
    print("Type 'quit' to exit")
    print("\nYou can ask me to:")
    print("- Add a new todo (e.g., 'Add a todo to buy groceries')")
    print("- List all todos (e.g., 'Show me all todos')")
    print("- Complete a todo (e.g., 'Mark todo #1 as completed')")
    print("- Delete a todo (e.g., 'Delete todo #1')")
    
    while True:
        query = input("\nWhat would you like to do? ")
        
        if query.lower() == 'quit':
            print("Goodbye!")
            break
        
        try:
            result = Runner.run_sync(
                agent,
                query,
            )
            print("\nAssistant:", result.final_output)
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main() 