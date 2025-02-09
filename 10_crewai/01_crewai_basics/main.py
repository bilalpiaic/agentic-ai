from crewai import Agent,Task, Crew,LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os
load_dotenv()

# call gemini model
llm = LLM(
    api_key=os.getenv("GOOGLE_API_KEY"),
    model="gemini/gemini-1.5-flash",
)
# Create tools
search_tool = SerperDevTool()


# Create an agent
agent1 = Agent(
    role = "Virtual Gym Trainer",
    goal="Help people to stay fit and healthy",
    backstory="I am a virtual gym trainer who is here to help you stay fit and healthy. I am here to guide you through your fitness journey and help you achieve your fitness goals.",
    llm=llm,
    memory=True,
    verbose=False,
    tools=[search_tool]
)

# Tasks
task1 = Task(
    name="Get to know the user",
    description="Get to know the user and their fitness goals",
    expected_output="Steps: How to lose weight and get in shape",
    tools=[search_tool],
    agent=agent1
)

# Execute the crew
crew = Crew(
    agents=[agent1],
    tasks=[task1],
    verbose=False
)

result = crew.kickoff()

print(result)
