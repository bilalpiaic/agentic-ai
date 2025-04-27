# Few-shot prompting is a technique in prompt engineering where a model is given a small number of examples (the "shots") to learn a specific task or pattern. These examples guide the model to generate desired outputs for new, similar inputs. It leverages the model's ability to generalize from limited data without requiring fine-tuning. This approach is useful for tasks like classification, translation, or text generation, where providing a few clear examples helps the model understand the context and produce accurate results. Few-shot prompting is efficient, flexible, and mimics how humans learn from examples.

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

user_input = input ("Enter input:")

# Define the few-shot prompt with examples
few_shot_prompt = f"""
Classify the sentiment of the following sentences as "positive", "negative", or "neutral".

Example 1:
Sentence: "I absolutely love this product! It's amazing."
Sentiment: positive

Example 2:
Sentence: "The service was terrible and the staff was rude."
Sentiment: negative

Example 3:
Sentence: "I ordered a coffee and it was delivered on time."
Sentiment: neutral

Now, classify this sentence:
Sentence: {user_input}
Sentiment:"""

# Invoke the LLM with the few-shot prompt
result = llm.invoke(few_shot_prompt)

# Print the result
print(result)