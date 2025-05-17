import json
from openai import AsyncOpenAI
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
def calculate_bill(unit: float) -> float:
    """Calculate the bill based on the number of units consumed.
    
    Args:
        unit: The number of units consumed.
    
    Returns:
        The calculated bill amount.
    """
    try:
        # Define the rate per unit
        print("Calculating bill...", unit)
        rate_per_unit = 0.5
        bill_amount = unit * rate_per_unit
        return bill_amount
    except Exception as e:
        raise ValueError(f"Error calculating bill: {e}")

agent = Agent(
    name="Bill Calculator Assistant",
    instructions="You are an expert calculator. you need to expected calculate bills for users based on their queries.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[calculate_bill],
)

query = input("Enter the query: ")

result = Runner.run_sync(
    agent,
    query,
)

print(result.final_output)

