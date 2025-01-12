from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()


chat_prompt_template = ChatPromptTemplate.from_messages(
    [     
        SystemMessage(content="You are a helpful booking hotel assistant, please response queries about booking hotels."),
    ]
)



llm = GoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY") # type: ignore
)



while True:
    user_input = input("You: ")
    if user_input == "exit":
        break
    chat_prompt_template.append(HumanMessage(content=user_input))
    chat_prompt = chat_prompt_template.format()
    print("Chat Prompt: ",chat_prompt)
    response = llm.invoke(chat_prompt)
    print("LLM Response",response) # type: ignore
    chat_prompt_template.append(AIMessage(content=response)) # type: ignore














# chat_message_prompt = ChatMessagePromptTemplate.from_template(
#     role="Jedi", template="May the {subject} be with you"
# )
# chat_message_prompt.format(subject="force")



chat_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="You are a helpful AI bot. Your name is {name}."),
        HumanMessage(content="Hello, how are you doing?"),
        AIMessage(content="I'm doing well, thanks!"),
        HumanMessage(content="{user_input}"),
    ]
)

messages_history = chat_prompt.format_messages(name="UniBot", user_input="What is your name?")

# print(messages_history)

chat_prompt_template = ChatPromptTemplate.from_messages(
    [     
         ("system", "You are a helpful AI bot. Your name is {name}."),
         ("human", "Hello, how are you doing?"),
         ("ai", "I'm doing well, thanks!"),
         ("human", "{user_input}"),
    ]
)

messages_history = chat_prompt_template.format_messages(name="UniBot", user_input="What is your name?")  
# print(messages_history)



# print(output)




prompt_template = PromptTemplate.from_template(
    "Tell me a {adjective} {joke} about {content}."
)

result = prompt_template.format(adjective="funny", content="chickens", joke="joke")

# print( result )

# How to get started for this file
# 1 -> uv init --no-workspace
# 2 -> uv add langchain_core
# 3 -> uv run python 01_langchain_prompts.py
# 4 -> uv add langchain_google_genai
# 5 -> uv add python-dotenv

