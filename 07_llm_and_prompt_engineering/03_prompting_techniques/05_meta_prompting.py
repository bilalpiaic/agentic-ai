from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the LLM
llm = GoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Step 1: Meta-Prompting - Generate a better prompt
meta_prompt = """
Your task is to create a better prompt for solving math word problems. The prompt should guide the model to break down the problem into clear, logical steps and provide the final answer.

Write a prompt that would help the model solve this problem step by step. Be clear and concise.
"""

# First LLM Call: Generate the improved prompt
generated_prompt = llm.invoke(meta_prompt)
print("Generated Prompt:\n", generated_prompt)

# Step 2: Use the generated prompt to solve the problem
# Define the problem to solve
problem = "Sarah has 15 apples. She gives 4 apples to her friend and then buys 10 more apples from the store. How many apples does Sarah have now?"

# Combine the generated prompt with the problem
final_prompt = f"{generated_prompt}\n\nProblem: {problem}"

# Second LLM Call: Solve the problem using the generated prompt
result = llm.invoke(final_prompt)
print("\nTest Result:\n", result)