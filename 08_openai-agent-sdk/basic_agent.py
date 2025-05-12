from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = AsyncOpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)

# Create an agent with specific instructions and model
agent = Agent(
    name="Assistant",
    instructions="""You are a helpful AI assistant that can:
    1. Answer questions accurately and concisely
    2. Provide explanations when needed
    3. Be friendly and professional in your responses""",
    model=OpenAIChatCompletionsModel(
        model="gpt-3.5-turbo",
        openai_client=client
    ),
)

def main():
    print("Welcome to the Basic Agent Demo!")
    print("Type 'quit' to exit")
    
    while True:
        # Get user input
        query = input("\nEnter your question: ")
        
        # Check if user wants to quit
        if query.lower() == 'quit':
            print("Goodbye!")
            break
        
        # Run the agent
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