#have to run this first: `uv add docling`

from crewai import LLM, Agent, Crew, Process, Task
from crewai.knowledge.source.crew_docling_source import CrewDoclingSource

# Create a knowledge source
content_source = CrewDoclingSource(
    file_paths=[
        "https://lilianweng.github.io/posts/2024-11-28-reward-hacking",
        "https://lilianweng.github.io/posts/2024-07-07-hallucination",
    ],
)

# Create an LLM with a temperature of 0 to ensure deterministic outputs
llm = LLM(model="gpt-4o-mini", temperature=0)

# Create an agent with the knowledge store
agent = Agent(
    role="About papers",
    goal="You know everything about the papers.",
    backstory="""You are a master at understanding papers and their content.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
)
task = Task(
    description="Answer the following questions about the papers: {question}",
    expected_output="An answer to the question.",
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential,
    knowledge_sources=[
        content_source
    ],  # Enable knowledge by adding the sources here. You can also add more sources to the sources list.
)

result = crew.kickoff(
    inputs={
        "question": "What is the reward hacking paper about? Be sure to provide sources."
    }
)