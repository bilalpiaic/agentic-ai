import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, RunContextWrapper
import os
from dataclasses import dataclass
from dotenv import load_dotenv
from typing import TypedDict
load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

@dataclass
class User:
  user_id: str


@function_tool  
async def get_user_info(ctx: RunContextWrapper[User]) -> str:
    
    """Fetches the user personal information to personalize responses. Whenver you require user personal info. call this function

    Args:
        id: The user unique indentifier
    """
    id = ctx.context.user_id
    if id == 1:
        user_info = "User name is Ali. He is 19 years old. He is a Agentic AI Engineer by profession. He likes playing Cricket."
    elif id == 2:
        user_info = "User name is Usman. He is 30 years old. He is a doctor by profession. He likes mountains."
    else:
        user_info = "user not found"

    return user_info

agent = Agent[User](
    name="Assistant",
    instructions="You are an expert of agentic AI.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[get_user_info]
)

query = input("Enter the query: ")

result = Runner.run_sync(
    agent,
    query,
    context=User(user_id=1)
)

print(result.final_output)