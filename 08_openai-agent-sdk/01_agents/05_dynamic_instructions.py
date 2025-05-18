import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, RunContextWrapper
import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

@dataclass
class UserContext:
  name: str

def dynamic_instructions(
    context: RunContextWrapper[UserContext], agent: Agent[UserContext]
) -> str:
    return f"The user's name is {context.context.name}. Help them with their questions."

agent = Agent[UserContext](
    name="Triage agent",
    instructions=dynamic_instructions,
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
)


query = input("Enter the query: ")

result = Runner.run_sync(
    agent,
    query,
    context=UserContext(name="Muhammad Zain Attiq")
)

print(result.final_output)
