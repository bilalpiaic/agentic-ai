import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner
from agents.mcp import MCPServerStdio

load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

async def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    samples_dir = os.path.join(current_dir, "sample_files")

    async with MCPServerStdio(
        name="Filesystem Server, via npx",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
        },
    ) as mcp_server:
        for tool in await mcp_server.list_tools():
            print(tool.name)
        agent = Agent(
            name="Assistant",
            instructions="You are an expert of agentic AI.",
            model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
            mcp_servers=[mcp_server],
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