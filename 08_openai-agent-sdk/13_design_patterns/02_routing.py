from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# --- Step 1: Define output format for routing ---
class SupportRoutingDecision(BaseModel):
    department: str  # "billing", "technical", or "general"
    query: str       # Reformulated query for the department agent


# --- Step 2: Routing Agent ---
support_router_agent = Agent(
    name="SupportRouter",
    instructions="""
You're a support router assistant. Read the user's message and classify it as one of:
- 'billing' (for refunds, invoices, payments),
- 'technical' (for app issues, bugs, login problems),
- 'general' (for store hours, location, contact info).

Return a JSON with:
- department: one of 'billing', 'technical', 'general'
- query: a cleaned-up version of the user's query that the department agent can act on.
""",
    output_type=SupportRoutingDecision,
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
)

# --- Step 3: Specialized Agents ---
billing_agent = Agent(
    name="BillingAgent",
    instructions="You are the billing department. Respond professionally to the given billing-related query.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
)

technical_agent = Agent(
    name="TechnicalSupportAgent",
    instructions="You are a technical support agent. Troubleshoot the issue described in the query.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
)

general_agent = Agent(
    name="GeneralInquiryAgent",
    instructions="Answer the user's general inquiry clearly and helpfully.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
)

# --- Step 4: Routing logic ---
def main():
    user_input = input("Enter your query: ")

    # Step 1: Classify the request
    route_result = Runner.run_sync(support_router_agent, user_input)
    decision = route_result.final_output

    print(f"\n📦 Routed to: {decision.department.capitalize()} Department")

    # Step 2: Send to the correct agent
    if decision.department == "billing":
        reply = Runner.run_sync(billing_agent, decision.query)
    elif decision.department == "technical":
        reply = Runner.run_sync(technical_agent, decision.query)
    elif decision.department == "general":
        reply = Runner.run_sync(general_agent, decision.query)
    else:
        print("❌ Unknown department. Cannot route.")
        return

    print("\n✅ Response:\n")
    print(reply.final_output)

if __name__ == "__main__":
    main()