# As we cover more and more examples and applications with prompt engineering, you will notice that certain elements make up a prompt.

# A prompt contains any of the following elements:

# Instruction - a specific task or instruction you want the model to perform

# Context - external information or additional context that can steer the model to better responses

# Input Data - the input or question that we are interested to find a response for

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

# Elements of the prompt
instruction = "Answer the user's question politely and provide accurate information."

context = (
    "You are a virtual assistant for Sunshine Hotel. The hotel offers a variety of amenities, "
    "including a swimming pool, free Wi-Fi, a fitness center, and an in-house restaurant."
)
input_data = (
    "Additional Information:\n"
    "- Check-in time: 2:00 PM\n"
    "- Check-out time: 11:00 AM\n"
    "- Address: 123 Beachside Lane, Miami, FL\n"
    "- Contact: +1-800-555-6789"
)
question = input("Enter ")

# Combine elements into a single prompt
prompt = f"{instruction}\n\n{context}\n\n{input_data}\n\nUser's Question: {question}"

# Invoke the LLM with the constructed prompt
result = llm.invoke(prompt)

# Print the result
print(result)


#To see examples: see here: https://www.promptingguide.ai/introduction/examples