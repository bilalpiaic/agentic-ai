from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()

llm = GoogleGenerativeAI(
     model="gemini-1.5-flash",
     google_api_key=os.getenv("GOOGLE_API_KEY")
)

result = llm.invoke("What is the capital of pakistan?")

print(result)

