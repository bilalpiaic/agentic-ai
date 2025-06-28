from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, handoff, RunContextWrapper
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


urdu_agent = Agent(
    name="Urdu agent",
    instructions="You only speak Urdu.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
)

def on_handoff(agent: Agent, ctx: RunContextWrapper[None]):
    agent_name = agent.name
    print("--------------------------------")
    print(f"Handing off to {agent_name}...")
    print("--------------------------------")


triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    handoffs=[
            handoff(urdu_agent, on_handoff=lambda ctx: on_handoff(urdu_agent, ctx)),
            handoff(english_agent, on_handoff=lambda ctx: on_handoff(english_agent, ctx))
    ],
)

history = []

while True:

    query = input("Enter the query: ")

    history.append({"role": "user", "content": query})

    result = Runner.run_sync(
        triage_agent,
        history,
    )

    li = result.to_input_list()
    
    history.extend(li)

    print(result.final_output)