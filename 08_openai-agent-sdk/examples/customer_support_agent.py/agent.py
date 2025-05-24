import time
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool
import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')
pinecone_api_key = os.getenv('PINECONE_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


def setup_db(pinecone_instance, index_name="testing"):
    if not pinecone_instance.has_index(index_name):
        print(f"Creating index {index_name}...")
        res = pinecone_instance.create_index_for_model(
            name=index_name,
            cloud="aws",
            region="us-east-1",
            embed={
                "model":"llama-text-embed-v2",
                "field_map":{"text": "chunk_text"}
            }
        )
    else:
        print(f"Index {index_name} already exists.")
    return "Index created successfully"

def split_into_word_chunks(text, chunk_size=100):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks
    
def insert_chunks_into_pinecone(index):
    data_dir = "data"
    record_counter = 1

    for file_name in os.listdir(data_dir):
        if file_name.endswith(".txt"):
            namespace = os.path.splitext(file_name)[0]  # namespace = file name without extension
            file_path = os.path.join(data_dir, file_name)

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read().replace("\n", " ").strip()  # Flatten text

            chunks = split_into_word_chunks(text, chunk_size=100)

            records = []
            for chunk in chunks:
                record = {
                    "_id": f"rec{record_counter}",
                    "chunk_text": chunk,
                    "category": namespace
                }
                records.append(record)
                record_counter += 1

            # Upsert to Pinecone using namespace
            index.upsert_records(namespace, records)
            print(f"Upserted {len(records)} records to namespace '{namespace}'")
            time.sleep(10)
            stats = index.describe_index_stats()
            print(stats)

    return "Inserted Successfully"

def query_pinecone(query, namespace):
    print(f"Querying Pinecone with query: {query}, namespace: {namespace}")
    pc = Pinecone(api_key=pinecone_api_key)
    index = pc.Index("testing")
    results = index.search(
        namespace=namespace,
        query={
            "top_k": 5,
            "inputs": {'text': query}
        }
    )
    print(f"Pinecone results: {results}")
    return results

sys_msg = """
You are EcoBot, the dedicated customer support AI for EcoHome Essentials, an e-commerce retailer specializing in sustainable home goods. Your role is to assist customers by providing accurate, concise, and helpful information based only on the knowledge base you have access to.

Core Directives and Behavioral Guidelines:

1. Strictly Data-Driven
Only respond with information available in the provided knowledge base.
You do not have access to:
- External sources
- Real-time data (e.g., current inventory or live order tracking)
- Personal customer accounts

2. Scope Limitation
If a user asks a question outside the scope of EcoHome Essentials (e.g., weather updates, movie recommendations, or unrelated products/policies), politely inform them that you can only assist with EcoHome Essentials-related topics. Offer to connect them with a human agent if their query is still about EcoHome Essentials but too complex for you to handle.

3. Tool Usage
You have access to four specialized tools to retrieve information from different categories of the knowledge base:
- get_order_shipping_info(query: str): For order placement, shipping, tracking, and delivery
- get_product_sustainability_info(query: str): For product details, sustainability, certifications, and care instructions
- get_returns_refunds_info(query: str): For returns, refunds, and exchanges
- get_account_tech_info(query: str): For account management, website issues, payments, and technical support

Always use the most appropriate tool to answer the user’s query accurately.

4. Clarity and Conciseness
Provide answers that are clear, direct, and easy to understand. Avoid technical jargon. Keep responses brief but complete.

5. Professional and Friendly Tone
Maintain a polite, respectful, and professional tone at all times.

6. Handling Ambiguity
If the user’s query is unclear or lacks detail, ask follow-up questions to clarify.
Examples:
- "Could you please specify which product you're asking about?"
- "Are you referring to an online order or an in-store purchase?"

7. Escalation Protocol
If a query requires access to sensitive personal information or order-specific details (e.g., "What is the status of order number 12345?"), inform the user that you cannot assist and recommend they contact a human support agent. Never guess or infer personal information.

8. Safety and Advice Boundaries
Do not provide any kind of professional advice, including:
- Medical
- Legal
- Financial
Your role is limited to providing information from the given data.

9. Limitations Communication
Do not apologize or mention that you are an AI model unless directly asked. Focus on delivering the best possible response within your capabilities.

Primary Objective:
Empower customers of EcoHome Essentials with fast, accurate, and easy-to-understand information, enhancing their ability to solve problems through self-service.
"""



@function_tool
def get_order_shipping_info(query: str) -> str:
    """
    Retrieves comprehensive information regarding order placement, processing, shipping methods,
    real-time tracking, and common delivery issues for EcoHome Essentials.

    This tool provides detailed answers to questions such as:
    - How to place an order and accepted payment methods.
    - What to expect regarding order confirmation and processing times.
    - Available shipping options (Standard, Expedited, Express) and international shipping policies.
    - How shipping costs are calculated.
    - Instructions for tracking an order, understanding tracking statuses, and troubleshooting
      issues like "delivered but not received" or delayed updates.
    - Procedures for handling damaged packages, lost packages, and undeliverable items due to
      incorrect addresses.
    - Policies on modifying or canceling orders after placement.

    Args:
        query (str): A natural language query or keyword related to order or shipping information.
                     While this tool returns the full text for now, in a more advanced
                     implementation, this query could be used to filter or highlight
                     relevant sections of the information.

    Returns:
        str: A detailed document containing all available information on EcoHome Essentials'
             order and shipping policies and procedures.
    """
    try:
        results = query_pinecone(query=query, namespace='order_and_shipping_info')
        return results
    except Exception as e:
        print(f"Error occurred: {e}")
        return "No relevant information found."


@function_tool
def get_product_sustainability_info(query: str) -> str:
    """
    Retrieves detailed information about EcoHome Essentials products, including their
    materials, sustainability aspects, certifications, ethical sourcing, care instructions,
    and environmental impact.

    This tool provides answers to questions such as:
    - General product inquiries like finding specific product details, durability, and care.
    - What makes products "sustainable" (renewable resources, low environmental impact, durability,
      non-toxic, ethical production, recyclability/compostability).
    - Information on ethical sourcing practices and supply chain vetting.
    - Details on third-party certifications (GOTS, FSC, OEKO-TEX, B Corp, Fair Trade).
    - Common materials used in products (Organic Cotton, Bamboo, Recycled Glass/Plastic/Metal, Hemp, Cork, Natural Rubber, Ceramics/Stoneware).
    - How products contribute to waste reduction (reusable alternatives, durability, recycled content,
      compostability, packaging).
    - Specific details for categories like eco-friendly cleaning products, organic cotton bedding,
      bamboo kitchenware, and reusable products (e.g., BPA-free, leak-proof).
    - Guidance on end-of-life disposal and recycling for products and packaging.

    Args:
        query (str): A natural language query or keyword related to product features,
                     sustainability, materials, or care instructions. While this tool
                     returns the full text for now, in a more advanced implementation,
                     this query could be used to filter or highlight relevant sections.

    Returns:
        str: A detailed document containing all available information on EcoHome Essentials'
             products, their sustainability aspects, and related details.
    """
    try:
        results = query_pinecone(query=query, namespace='product_info')
        return results
    except Exception as e:
        print(f"Error occurred: {e}")
        return "No relevant information found."


@function_tool
def get_returns_refunds_info(query: str) -> str:
    """
    Retrieves detailed information about EcoHome Essentials' return, refund, and exchange policies.

    This tool provides answers to questions such as:
    - The general return policy, including the return window and receipt requirements.
    - Procedures for returning items, including how to initiate a return and where to send items.
    - Information on who covers return shipping costs (customer vs. company error).
    - Details on how refunds are issued (original payment method, gift card) and processing times.
    - Policies regarding exchanges for different sizes, colors, or products.
    - Specific conditions and exceptions for returns (e.g., non-returnable items, electronics,
      personal care items, "final sale" items).
    - What to do if an item arrives damaged or defective.
    - Handling returns for items purchased as gifts or part of promotional offers.

    Args:
        query (str): A natural language query or keyword related to returns, refunds, or exchanges.
                     While this tool returns the full text for now, in a more advanced
                     implementation, this query could be used to filter or highlight
                     relevant sections.

    Returns:
        str: A detailed document containing all available information on EcoHome Essentials'
             returns, refunds, and exchanges policies.
    """
    try:
        results = query_pinecone(query=query, namespace='return_refund_and_exchanges_info')
        return results
    except Exception as e:
        print(f"Error occurred: {e}")
        return "No relevant information found."


@function_tool
def get_account_tech_info(query: str) -> str:
    """
    Retrieves information related to managing an EcoHome Essentials online account,
    website functionality, payment issues, privacy, security, and general technical support.

    This tool provides answers to questions such as:
    - How to create, access, update, or delete an online account.
    - Password reset procedures.
    - Benefits of having an account versus guest checkout.
    - Website navigation and functionality (e.g., search, applying discount codes).
    - Troubleshooting common website issues like items not adding to cart or pages not loading.
    - Information on website security and data protection (SSL encryption, privacy policy).
    - Payment methods accepted online and troubleshooting failed payments.
    - Managing email preferences and communication.
    - Reporting security vulnerabilities or suspicious activity.
    - General technical assistance for online shopping.

    Args:
        query (str): A natural language query or keyword related to account management,
                     technical issues, website functionality, or privacy/security. While
                     this tool returns the full text for now, in a more advanced
                     implementation, this query could be used to filter or highlight
                     relevant sections.

    Returns:
        str: A detailed document containing all available information on EcoHome Essentials'
             account management, technical support, and privacy policies.
    """
    try:
        results = query_pinecone(query=query, namespace='account_and_technical_info')
        return results
    except Exception as e:
        print(f"Error occurred: {e}")
        return "No relevant information found."


if __name__ == "__main__":
    pc = Pinecone(api_key=pinecone_api_key)
    

    setup_db(pc, index_name="testing")

    index = pc.Index("testing")
    
    print("Waiting for index to be ready...")
    for _ in range(12):
        stats = index.describe_index_stats()
        print(stats)
        if stats.get("total_vector_count", 0) >= 50:
            break
        time.sleep(5)

    insert_chunks_into_pinecone(index)

    # 4. Wait for vectors to be fully indexed
    print("Ensuring vectors are indexed...")
    for _ in range(10):
        stats = index.describe_index_stats()
        print(stats)
        if stats["total_vector_count"] >= 50:
            break
        time.sleep(5)

    agent = Agent(
        name="Assistant",
        instructions=sys_msg,
        model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
        tools=[get_order_shipping_info, get_product_sustainability_info, get_returns_refunds_info, get_account_tech_info]
    )

    history = []

    while True:

        query = input("Enter the query: ")

        history.append({"role": "user", "content": query})

        result = Runner.run_sync(
            agent,
            history,
        )

        li = result.to_input_list()
        history.extend(li)

        print(result.final_output)