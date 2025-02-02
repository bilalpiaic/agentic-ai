# Top P - A sampling technique with temperature, called nucleus sampling, where you can control how deterministic the model is. If you are looking for exact and factual answers keep this low. If you are looking for more diverse responses, increase to a higher value. If you use Top P it means that only the tokens comprising the top_p probability mass are considered for responses, so a low top_p value selects the most confident responses. This means that a high top_p value will enable the model to look at more possible words, including less likely ones, leading to more diverse outputs.

# The general recommendation is to alter temperature or Top P but not both.

from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()

top_p = float(input("Enter LLM Top_k: "))

llm = GoogleGenerativeAI(
     model="gemini-1.5-flash",
     google_api_key=os.getenv("GOOGLE_API_KEY"),
     top_p=top_p
)

question = input("Enter you prompt: ")

response = llm.invoke(question)

print("Response", response)
