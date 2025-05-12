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


urdu_agent = Agent(
    name="Assistant",
    instructions="You are a urdu translator agent. Translate the user message to Urdu.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
)

spanish_agent = Agent(
    name="Assistant",
    instructions="You are a spanish translator agent. Translate the user message to Spanish.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
)

main_agent = Agent(
    name="Assistant",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools in order."
        "You never translate on your own, you always use the provided tools."
    ),
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[
        urdu_agent.as_tool(
            tool_name="translate_to_urdu",
            tool_description="Translate the user's message to Urdu",
        ),
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        )
        ]
)

while True:
    query = input("Enter the query: ")

    result = Runner.run_sync(
        main_agent,
        query,
    )

    print(result.final_output)