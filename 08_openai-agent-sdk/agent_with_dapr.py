import os
import requests
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner

# Load environment variables
load_dotenv()

# OpenAI Client Setup
gemini_api_key = os.getenv('GEMINI_API_KEY')
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Dapr Settings
DAPR_STATE_STORE_URL = "http://localhost:3500/v1.0/state/statestore"
MEMORY_KEY = "last_agent_response"

# Agent Setup
agent = Agent(
    name="Assistant",
    instructions="You are an expert of agentic AI.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
)

def read_memory_from_dapr():
    try:
        resp = requests.get(f"{DAPR_STATE_STORE_URL}/{MEMORY_KEY}")
        if resp.status_code == 200:
            memory = resp.json()
            print("\n[Previous Session]")
            print(f"Query: {memory.get('query')}")
            print(f"Response: {memory.get('response')}\n")
        else:
            print("\n[Previous Session] No previous memory found.\n")
    except Exception as e:
        print(f"[Dapr] Error reading memory: {e}")

def write_memory_to_dapr(query, response):
    payload = [
        {
            "key": MEMORY_KEY,
            "value": {
                "query": query,
                "response": response
            }
        }
    ]
    try:
        resp = requests.post(DAPR_STATE_STORE_URL, json=payload)
        if resp.status_code == 204:
            print("[Dapr] Memory saved successfully!\n")
        else:
            print(f"[Dapr] Failed to save memory: {resp.text}")
    except Exception as e:
        print(f"[Dapr] Error saving memory: {e}")

def main():
    print("----- Agent with Dapr State -----")

    # Step 1: Read and show last memory
    read_memory_from_dapr()

    # Step 2: Get user input
    query = input("Enter your new query: ")

    # Step 3: Run agent
    result = Runner.run_sync(agent, query)
    print("\n[Agent Response]")
    print(result.final_output)

    # Step 4: Save new result to Dapr
    write_memory_to_dapr(query, result.final_output)

if __name__ == "__main__":
    main()