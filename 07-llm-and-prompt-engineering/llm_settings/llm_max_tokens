# Max Length - You can manage the number of tokens the model generates by adjusting the max length. Specifying a max length helps you prevent long or irrelevant responses and control costs.

from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()

max_output_tokens = input("Enter maximum tokens:")

llm = GoogleGenerativeAI(
     model="gemini-1.5-flash",
     google_api_key=os.getenv("GOOGLE_API_KEY"),
     max_output_tokens=max_output_tokens
)



question = input("Enter you prompt: ")

response = llm.invoke(question)

print("Response", response)
