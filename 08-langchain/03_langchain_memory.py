from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory, ConversationSummaryMemory, ConversationSummaryBufferMemory
from langchain.chains import ConversationChain
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv  
import os
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

memory1 = ConversationBufferMemory()
memory2 = ConversationBufferWindowMemory(k = 2)
memory3 = ConversationSummaryMemory(llm=llm)
memory4 = ConversationSummaryBufferMemory(llm=llm, max_token_limit=1000)

# Put here the memory which one you want to use
chain = ConversationChain(llm=llm, memory=memory1)

while True: 
    user_input = input("You: ")
    if user_input == "exit":
        break
    response = chain.invoke(user_input)
    print("Final==>>",response)



























# from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory,ConversationSummaryMemory, ConversationSummaryBufferMemory
# from langchain.chains import ConversationChain
# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# import os
# load_dotenv()

# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))


# memory = ConversationBufferMemory()


# chain = ConversationChain(llm=llm, memory=memory)

# while True: 
#     user_input = input("You: ")
#     if user_input == "exit":
#         break
#     response = chain.invoke(user_input, user="123")
#     print("Final==>>",response)






