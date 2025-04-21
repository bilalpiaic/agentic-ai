import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool
import os
from dotenv import load_dotenv
from typing import TypedDict
load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

class Location(TypedDict):
    city_name: str

@function_tool  
async def fetch_weather(location: Location) -> str:
    
    """Fetch the weather for a given location.

    Args:
        location: The location to fetch the weather for.
    """
    # In real life, we'd fetch the weather from a weather API
    return "sunny"


agent = Agent(
    name="Assistant",
    instructions="You are an expert of agentic AI.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[fetch_weather]
)

query = input("Enter the query: ")

result = Runner.run_sync(
    agent,
    query,
)

print(result.final_output)