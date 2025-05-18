from agents import Agent, Runner, OpenAIChatCompletionsModel, trace, set_default_openai_api, set_default_openai_client, set_tracing_disabled
import asyncio
import os
from openai import AsyncOpenAI

from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    
)

set_default_openai_client(client=client, use_for_tracing=True)
set_default_openai_api("chat_completions")

async def main():
    agent = Agent(name="Joke generator", instructions="Tell funny jokes.", model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),)

    with trace("Joke workflow"): 
        first_result = await Runner.run(agent, "Tell me a joke")
        second_result = await Runner.run(agent, f"Rate this joke: {first_result.final_output}")
        print(f"Joke: {first_result.final_output}")
        print(f"Rating: {second_result.final_output}")

asyncio.run(main())