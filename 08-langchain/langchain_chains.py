
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain, LLMChain
from dotenv import load_dotenv

import os
load_dotenv()

llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API"))

llm2 = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    huggingfacehub_api_token= os.getenv("HUGGINGFACE_TOKEN")
)



prompt0 = PromptTemplate(template="Context: of this chat", inputVriable=["chat"])



prompt1 = PromptTemplate(template="Give me the famous place of {Text}", inputVriable=["text"])

prompt2 = PromptTemplate(template="Wha is the location of place {text}", inputVriable=["text"])



chain1 = LLMChain(llm=llm, prompt=prompt1)
chain2 = LLMChain(llm=llm, prompt=prompt2)

chain = SimpleSequentialChain(chains=[chain1, chain2])

result = chain.invoke("Faisalabad")

print(result)




# from langchain_huggingface import HuggingFaceEndpoint

# llm = HuggingFaceEndpoint(
#     repo_id="HuggingFaceH4/zephyr-7b-beta"
#     huggingfacehub_api_token= "sdf"
# )