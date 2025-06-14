import asyncio
from agents import Agent, Runner, ItemHelpers, MessageOutputItem
from openai import AsyncOpenAI
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel 
import os
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You translate the user's message to Spanish",
    handoff_description="An english to spanish translator",
    model=model
)

french_agent = Agent(
    name="french_agent",
    instructions="You translate the user's message to French",
    handoff_description="An english to french translator",
    model=model
)

italian_agent = Agent(
    name="italian_agent",
    instructions="You translate the user's message to Italian",
    handoff_description="An english to italian translator",
    model=model
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools in order."
        "You never translate on your own, you always use the provided tools."
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
        italian_agent.as_tool(
            tool_name="translate_to_italian",
            tool_description="Translate the user's message to Italian",
        ),
    ],
    model=model,
)

synthesizer_agent = Agent(
    name="synthesizer_agent",
    instructions="You inspect translations, correct them if needed, and produce a final concatenated response. Always return the final response in with properly formatted translations.",
    model=model,
)


async def main():
    msg = input("Hi! What would you like translated, and to which languages? ")

    # Run the entire orchestration in a single trace
    orchestrator_result = await Runner.run(orchestrator_agent, msg)

    for item in orchestrator_result.new_items:
        if isinstance(item, MessageOutputItem):
            text = ItemHelpers.text_message_output(item)
            if text:
                print(f"  - Translation step: {text}")

    synthesizer_result = await Runner.run(
        synthesizer_agent,
         (orchestrator_result.to_input_list() + [{"role": "user", 'content': f'pick best translation done for these {msg}' }])
    )

    print(f"\n\nFinal response:\n{synthesizer_result.final_output}")

    return synthesizer_result, orchestrator_result


if __name__ == "__main__":
    asyncio.run(main())