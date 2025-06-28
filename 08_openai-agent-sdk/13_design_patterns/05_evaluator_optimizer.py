import asyncio
from agents import Agent, Runner, ItemHelpers
from openai import AsyncOpenAI
from pydantic import BaseModel
from typing import Literal
from dataclasses import dataclass
import os
from dotenv import load_dotenv
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel

# Load environment variables
load_dotenv()

# Create client
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Use Gemini Flash model
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)

# --- Optimizer Agent ---
story_outline_generator = Agent(
    name="StoryOutlineGenerator",
    instructions=(
        "You generate a short story outline based on the user's input. "
        "If feedback is provided, incorporate it to improve the outline."
    ),
    model=model,
)

# --- Evaluator Output Type ---
@dataclass
class EvaluationFeedback:
    status: Literal["pass", "needs_improvement", "fail"]
    feedback: str

# --- Evaluator Agent ---
evaluator = Agent(
    name="Evaluator",
    instructions=(
        "You evaluate a story outline. "
        "If it is not good enough, give clear and actionable feedback. "
        "Never rate an outline as 'pass' on the first try."
    ),
    output_type=EvaluationFeedback,
    model=model,
)

# --- Main Workflow Loop ---
async def main():
    user_request = input("What kind of story would you like to hear? ")

    input_items = [{"content": user_request, "role": "user"}]
    latest_outline = None

    while True:
        # Step 1: Generate or improve outline
        story_result = await Runner.run(story_outline_generator, input_items)
        latest_outline = ItemHelpers.text_message_outputs(story_result.new_items)
        print("\n📝 Generated Story Outline:\n", latest_outline)

        # Step 2: Evaluate the outline
        evaluation_result = await Runner.run(evaluator, story_result.to_input_list())
        feedback: EvaluationFeedback = evaluation_result.final_output

        print("--------------------------------------------------")
        print(f"\n🔎 Evaluator Status: {feedback.status}")
        print(f"💬 Feedback: {feedback.feedback}")
        print("--------------------------------------------------")

        if feedback.status == "pass":
            print("\n✅ Story outline approved. Workflow complete.")
            break

        # Step 3: Add feedback to input for next optimization loop
        print("\n🔁 Re-running generator with evaluator feedback...")
        input_items = story_result.to_input_list()
        input_items.append({"content": f"Feedback: {feedback.feedback}", "role": "user"})

    print("\n🎉 Final Optimized Story Outline:\n", latest_outline)


if __name__ == "__main__":
    asyncio.run(main())