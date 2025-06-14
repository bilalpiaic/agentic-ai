import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

def setup_database():
    # Load environment variables
    load_dotenv()
    
    # Get database URL from environment variable
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL not found in .env file")

    try:
        # Connect to the database
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()

        # Create expenses table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS expenses (
            id SERIAL PRIMARY KEY,
            amount DECIMAL(10,2) NOT NULL,
            description TEXT NOT NULL,
            category VARCHAR(50) NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        cur.execute(create_table_query)
        conn.commit()
        print("Database setup completed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    setup_database() 