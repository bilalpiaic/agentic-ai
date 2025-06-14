import os
from dotenv import load_dotenv
import psycopg2
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from agents import Agent, OpenAIChatCompletionsModel, function_tool, Runner
from openai import AsyncOpenAI

load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')


client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

# Database connection
def get_db_connection():
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL not found in .env file")
    return psycopg2.connect(database_url)

@function_tool
def add_expense(amount: float, description: str, category: str) -> str:
    """Add a new expense to the database."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
        INSERT INTO expenses (amount, description, category)
        VALUES (%s, %s, %s)
        RETURNING id;
        """
        cur.execute(query, (amount, description, category))
        expense_id = cur.fetchone()[0]
        conn.commit()
        
        return f"Successfully added expense with ID: {expense_id}"
    except Exception as e:
        return f"Error adding expense: {str(e)}"
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@function_tool
def get_expenses(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    category: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None
) -> List[Dict]:
    """Get expenses with optional filters."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = "SELECT * FROM expenses WHERE 1=1"
        params = []
        
        if start_date:
            query += " AND created_at >= %s"
            params.append(start_date)
        if end_date:
            query += " AND created_at <= %s"
            params.append(end_date)
        if category:
            query += " AND category = %s"
            params.append(category)
        if min_amount:
            query += " AND amount >= %s"
            params.append(min_amount)
        if max_amount:
            query += " AND amount <= %s"
            params.append(max_amount)
            
        query += " ORDER BY created_at DESC"
        
        cur.execute(query, params)
        columns = [desc[0] for desc in cur.description]
        expenses = [dict(zip(columns, row)) for row in cur.fetchall()]
        
        return expenses
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@function_tool
def update_expense(
    expense_id: int,
    amount: Optional[float] = None,
    description: Optional[str] = None,
    category: Optional[str] = None
) -> str:
    """Update an existing expense."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        updates = []
        params = []
        
        if amount is not None:
            updates.append("amount = %s")
            params.append(amount)
        if description is not None:
            updates.append("description = %s")
            params.append(description)
        if category is not None:
            updates.append("category = %s")
            params.append(category)
            
        if not updates:
            return "No updates provided"
            
        updates.append("updated_at = CURRENT_TIMESTAMP")
        query = f"""
        UPDATE expenses 
        SET {', '.join(updates)}
        WHERE id = %s
        RETURNING id;
        """
        params.append(expense_id)
        
        cur.execute(query, params)
        if cur.rowcount == 0:
            return f"No expense found with ID: {expense_id}"
            
        conn.commit()
        return f"Successfully updated expense with ID: {expense_id}"
    except Exception as e:
        return f"Error updating expense: {str(e)}"
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@function_tool
def delete_expense(expense_id: int) -> str:
    """Delete an expense by ID."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = "DELETE FROM expenses WHERE id = %s RETURNING id;"
        cur.execute(query, (expense_id,))
        
        if cur.rowcount == 0:
            return f"No expense found with ID: {expense_id}"
            
        conn.commit()
        return f"Successfully deleted expense with ID: {expense_id}"
    except Exception as e:
        return f"Error deleting expense: {str(e)}"
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@function_tool
def get_expense_summary(
    period: str = "month",
    category: Optional[str] = None
) -> Dict:
    """Get summary of expenses for a given period."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        if period == "month":
            start_date = datetime.now().replace(day=1)
        elif period == "week":
            start_date = datetime.now() - timedelta(days=datetime.now().weekday())
        elif period == "year":
            start_date = datetime.now().replace(month=1, day=1)
        else:
            return {"error": "Invalid period. Use 'week', 'month', or 'year'"}
            
        query = """
        SELECT 
            COUNT(*) as total_expenses,
            SUM(amount) as total_amount,
            AVG(amount) as average_amount,
            MIN(amount) as min_amount,
            MAX(amount) as max_amount
        FROM expenses
        WHERE created_at >= %s
        """
        params = [start_date]
        
        if category:
            query += " AND category = %s"
            params.append(category)
            
        cur.execute(query, params)
        summary = dict(zip([desc[0] for desc in cur.description], cur.fetchone()))
        
        # Get category breakdown
        category_query = """
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE created_at >= %s
        """
        if category:
            category_query += " AND category = %s"
        category_query += " GROUP BY category ORDER BY total DESC"
        
        cur.execute(category_query, params)
        summary['category_breakdown'] = dict(cur.fetchall())
        
        return summary
    except Exception as e:
        return {"error": str(e)}
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@function_tool
def search_expenses(search_term: str) -> List[Dict]:
    """Search expenses by description or category."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
        SELECT * FROM expenses 
        WHERE description ILIKE %s 
        OR category ILIKE %s
        ORDER BY created_at DESC
        """
        search_pattern = f"%{search_term}%"
        cur.execute(query, (search_pattern, search_pattern))
        
        columns = [desc[0] for desc in cur.description]
        expenses = [dict(zip(columns, row)) for row in cur.fetchall()]
        
        return expenses
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

agent = Agent(
    name="ExpenseTracker",
    instructions="""You are an expense tracking assistant. You can help users:
    1. Add new expenses
    2. View and search expenses
    3. Update existing expenses
    4. Delete expenses
    5. Get expense summaries and analytics
    6. Search through expenses
    
    Always be helpful and provide clear explanations of what you're doing.""",
    model=model,
    tools=[
        add_expense,
        get_expenses,
        update_expense,
        delete_expense,
        get_expense_summary,
        search_expenses
    ]
)


history = []

while True:

    query = input("Enter the query: ")

    history.append({"role": "user", "content": query})

    result = Runner.run_sync(
        agent,
        history,
    )

    li = result.to_input_list()
    
    history.extend(li)

    print(result.final_output)