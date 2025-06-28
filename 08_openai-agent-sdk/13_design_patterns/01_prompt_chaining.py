from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

# Setup Gemini client
gemini_api_key = os.getenv("GEMINI_API_KEY")
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Agent 1: Generate blog outline
blog_outline_agent = Agent(
    name="BlogOutliner",
    instructions="Create a clear and structured outline for a blog post based on the given topic. ",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
)

# Agent 2: Write blog post based on outline + references
blog_writer_agent = Agent(
    name="BlogWriter",
    instructions="Write a full blog post using the given outline and references.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
)

# Agent 3: Review the post and return a score + comments
class BlogReviewOutput(BaseModel):
    score: int
    comments: str

blog_review_agent = Agent(
    name="BlogReviewer",
    instructions="Evaluate the blog post for clarity and quality. Give a score out of 10 and provide feedback.",
    output_type=BlogReviewOutput,
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
)

# Synchronous flow
def main():
    topic = input("Enter the topic of your blog post: ")
    references = input("Enter any references you'd like to include (optional): ")

    # Step 1: Generate outline
    outline_result = Runner.run_sync(blog_outline_agent, topic)
    print("--------------------------------------------------")
    print("\n✅ Blog Outline:\n", outline_result.final_output)
    print("--------------------------------------------------")

    # Step 2: Generate blog post
    combined_input = f"Outline:\n{outline_result.final_output}\n\nReferences:\n{references}"
    blog_result = Runner.run_sync(blog_writer_agent, combined_input)
    print("--------------------------------------------------")
    print("\n✅ Blog Post Drafted.\n", blog_result.final_output)
    print("--------------------------------------------------")

    # Step 3: Review blog post
    review_result = Runner.run_sync(blog_review_agent, blog_result.final_output)
    review = review_result.final_output

    print("--------------------------------------------------")
    print(f"\n📝 Score: {review.score}/10")
    print(f"💬 Comments: {review.comments}")
    print("--------------------------------------------------")

    if review.score < 5:
        print("\n❌ Blog post quality too low. Exiting.")
        return

    print("\n✅ Blog post accepted!\n")
    print("📄 Final Blog Post:\n")
    print(blog_result.final_output)

if __name__ == "__main__":
    main()