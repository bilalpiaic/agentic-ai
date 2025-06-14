import asyncio
from agents import Agent, Runner, ItemHelpers
from openai import AsyncOpenAI
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Three independent Urdu translation agents (could have slightly different instructions or temperature)
urdu_agent_1 = Agent(
    name="UrduAgent1",
    instructions="Translate the user's message to Urdu, providing a clear and natural translation.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
)

urdu_agent_2 = Agent(
    name="UrduAgent2",
    instructions="Translate the user's message into fluent Urdu, maintaining the meaning accurately.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
)

urdu_agent_3 = Agent(
    name="UrduAgent3",
    instructions="Provide a natural and idiomatic Urdu translation of the user's input.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
)

# Agent to pick the best Urdu translation
translation_picker = Agent(
    name="TranslationPicker",
    instructions="""
Given the original English input and three Urdu translation options, select the best translation.
Explain briefly why it is the best.
Output only the best translation and your explanation.
""",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
)


async def main():
    msg = input("Hi! Enter a message to translate to Urdu:\n\n")

    # Run the three translation agents in parallel
    res1, res2, res3 = await asyncio.gather(
        Runner.run(urdu_agent_1, msg),
        Runner.run(urdu_agent_2, msg),
        Runner.run(urdu_agent_3, msg),
    )

    # Extract text outputs from agents
    translations = [
        ItemHelpers.text_message_outputs(res1.new_items),
        ItemHelpers.text_message_outputs(res2.new_items),
        ItemHelpers.text_message_outputs(res3.new_items),
    ]

    print("\n--- Translations ---\n")
    for i, t in enumerate(translations, start=1):
        print(f"Option {i}:\n{t}\n")

    # Prepare input for picker agent
    picker_input = (
        f"Original English message: {msg}\n\n"
        f"Translations:\n"
        f"1. {translations[0]}\n"
        f"2. {translations[1]}\n"
        f"3. {translations[2]}"
    )

    # Run picker agent to choose best translation
    best_translation_result = await Runner.run(translation_picker, picker_input)

    print("\n--- Best Translation Selected ---\n")
    print(best_translation_result.final_output)


if __name__ == "__main__":
    asyncio.run(main())