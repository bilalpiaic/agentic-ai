# Large language models (LLMs) today, such as GPT-3.5 Turbo, GPT-4, and Claude 3, are tuned to follow instructions and are trained on large amounts of data. Large-scale training makes these models capable of performing some tasks in a "zero-shot" manner. Zero-shot prompting means that the prompt used to interact with the model won't contain examples or demonstrations. The zero-shot prompt directly instructs the model to perform a task without any additional examples to steer it.

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

