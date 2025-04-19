"First must run your mcp server..."
import asyncio
import os
import subprocess
import shutil
import time
from typing import Any
from agents import Agent, OpenAIChatCompletionsModel, Runner
from agents.mcp import MCPServerSse
from agents.model_settings import ModelSettings
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key="AIzaSyC-lLOKX2NSFRSDdaUjLzotksgWnxYqEgw",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

async def main():
    # Connect to the running SSE server
    async with MCPServerSse(
        name="Filesystem Server via SSE",
        params={
            "url": "http://localhost:8000/sse",
        },
    ) as mcp_server:

        for tool in await mcp_server.list_tools():
            print(f"✅ Tool loaded from server: {tool.name}")

        agent = Agent(
            name="Assistant",
            instructions="You are an expert of agentic AI.",
            mcp_servers=[mcp_server],
            model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
        )

        while True:
            query = input("Enter the query: ")
            result = await Runner.run(
                starting_agent=agent,
                input=query,
            )
            print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())