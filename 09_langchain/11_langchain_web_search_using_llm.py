from langchain_community.tools.tavily_search import TavilySearchResults


tavily_search = TavilySearchResults(max_results=3)
search_docs = tavily_search.invoke("What is LangGraph?")
