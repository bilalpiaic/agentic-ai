from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool
import os
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


@function_tool  
def get_refund(amount) -> str:
    """Fetch the refund status for a given amount.

    Args:
        amount: The amount to fetch the refund status for.
    """
    print(f"Fetching refund status for {amount}...")
    return "Refund approved"

@function_tool
def book_flight(location) -> str:
    """Book a flight for a given location.

    Args:
        location: The location to book the flight for.
    """
    print(f"Booking flight for {location}...")
    # In real life, we'd book the flight through a flight API
    return "Flight booked successfully."


booking_agent = Agent(
    name="Booking agent",
    instructions="You are a booking agent.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[book_flight],
)
refund_agent = Agent(
    name="Refund agent",
    instructions="You are a refund agent.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[get_refund],
)

triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "Help the user with their questions."
        "If they ask about booking, handoff to the booking agent."
        "If they ask about refunds, handoff to the refund agent."
    ),
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    handoffs=[booking_agent, refund_agent],
)

query = input("Enter the query: ")

result = Runner.run_sync(
    triage_agent,
    query,
)

print(result.final_output)
