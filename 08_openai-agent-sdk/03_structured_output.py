from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List

load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

class Quiz(BaseModel):
    question: str
    options: List[str]  # ✅ Now Gemini knows it's a list of strings
    correct_option: str

agent = Agent(
    name="Assistant",
    instructions="You are a Quiz Agent. You generate quizes",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    # output_type=Quiz
)

query = input("Enter the query: ")

result = Runner.run_sync(
    agent,
    query,
)

print(result.final_output)