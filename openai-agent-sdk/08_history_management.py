import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


agent = Agent(
    name="Assistant",
    instructions="You are an expert of agentic AI.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
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
    print("li", history)

    print(result.final_output)