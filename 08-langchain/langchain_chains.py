
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain, LLMChain
from dotenv import load_dotenv

import os
load_dotenv()


# llm_for_keyword = HuggingFaceEndpoint(
#     repo_id="HuggingFaceH4/zephyr-7b-beta",
#     huggingfacehub_api_token= os.getenv("HUGGINGFACE_TOKEN")
# )

llm = GoogleGenerativeAI(
     model="gemini-1.5-flash",
     google_api_key=os.getenv("GOOGLE_API_KEY")
)

# llm_for_description = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API"))




prompt_for_keywords = PromptTemplate(template="Define keyword for article writing, user give the article title is: {input}", input_variables=["input"])

prompt_for_outline = PromptTemplate(template="Write outline for an article using keywords {input}", input_variables=["input"])

prompt_for_description = PromptTemplate(template="Write the detailed article following the provided outline is: {input}", input_variables=["input"])



keywords_step = LLMChain(llm=llm, prompt=prompt_for_keywords)
outline_step = LLMChain(llm=llm, prompt=prompt_for_outline)
description_step = LLMChain(llm=llm, prompt=prompt_for_description)

chain = SimpleSequentialChain(chains=[keywords_step, outline_step, description_step])

result = chain.invoke({"input": "what is the best way to learn programming?"})

print(result)



