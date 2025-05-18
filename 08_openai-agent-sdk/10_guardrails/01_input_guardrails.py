from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
)
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
)


@input_guardrail
async def math_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        # tripwire_triggered=False #result.final_output.is_math_homework,
        tripwire_triggered=result.final_output.is_math_homework,
    )


agent = Agent(
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    input_guardrails=[math_guardrail],
)

query = input("Enter the query: ")

try:
    result = Runner.run_sync(
        agent,
        query,
    )
    print(result.final_output)
except InputGuardrailTripwireTriggered:
    print("Math homework guardrail tripped")

