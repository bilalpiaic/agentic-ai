
# How to get started
- Poetry configuration 

- Poetry install https://python-poetry.org/docs/#installing-with-the-official-installer

``` curl -sSL https://install.python-poetry.org | python3 - ```

- For window install using powershell
  
  ``` (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py - ```

- Install all project dependencies ( already created project)
```
poetry install --no-root
```

- To create a new project
   ``` poetry init ```

- To install new dependencies 
   ``` poetry add package-name ```

- To remove dependencies 
   ``` poetry remove package-name ```


## How to install Fast API
``` 
poetry add "fastapi[standard]"
poetry add uvicorn

 ```

## How to run files
- Run using python
  `poetry run python relatativepath`
  e.g

  ```poetry run python 07-llm-and-prompt-engineering/01_gemeni_llm.py ```

- Run using fastapi / uvicorn
   `poetry run uvicorn relativepath:app --reload` change forward slash to dot. and .py to :app 
   e.g

   ```poetry run uvicorn 09-langgraph.websocket-agent.ws_agent_server_gemini:app --reload```



## Course Outline

Cloud native Applied AI Agentic Developer
1- Python 
2- AI Theory - Terminologies
3- Fast API 
4- Database ( SQL, No SQL ) 
5- Third Party libraries, Numpy, pandas, opencv
6- Model development lifecycle - Keras
7- LLM - Gemeni / OpenAI / Allama 
8- LLM Framework - Langchain
9- Agentic Framework - Langgraph
10- Cloud computing / devops - docker, kubernetes 
11- Frontend Nextjs - chatbot UI / Agent frontend

![alt text](outline.png)
