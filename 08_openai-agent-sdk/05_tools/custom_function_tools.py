from typing import Any
from pydantic import BaseModel
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, RunContextWrapper, FunctionTool
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

def fetch_weather_data(city: str, unit: str) -> str:
    # replace with actual API call
    return f"The weather in {city} is 25°{unit.upper()} (simulated)."

class WeatherArgs(BaseModel):
    city: str
    unit: str 

async def run_fetch_weather(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = WeatherArgs.model_validate_json(args)
    return fetch_weather_data(city=parsed.city, unit=parsed.unit)

fetch_weather_tool = FunctionTool(
    name="fetch_weather",
    description="Returns the current weather for a given city and unit (C or F).",
    params_json_schema=WeatherArgs.model_json_schema(),
    on_invoke_tool=run_fetch_weather,
)


agent = Agent(
    name="Assistant",
    instructions="You are a weather assistant..",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[fetch_weather_tool]
)

query = input("Enter the query: ")

result = Runner.run_sync(
    agent,
    query
)

print(result.final_output)