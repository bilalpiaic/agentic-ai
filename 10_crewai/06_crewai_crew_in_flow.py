from crewai import Agent,Task, Crew,LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel


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
    description="user goal is: {content}",
    expected_output="Steps:",
    tools=[search_tool],
    agent=agent1
)

# Execute the crew
crew = Crew(
    agents=[agent1],
    tasks=[task1],
    verbose=False
)





class ExampleState(BaseModel):
    counter: int = 0
    message: str = ""

class StateExampleFlow(Flow[ExampleState]):

    @start()
    def first_method(self):
        result = crew.kickoff(inputs={"content": "i want to gain muscle give me steps"}) 
        self.state.message = result.raw
        self.state.counter += 1

    @listen(first_method)
    def second_method(self):
        self.state.message += " - updated by second_method"
        self.state.counter += 1
        return self.state.message

flow = StateExampleFlow()
final_output = flow.kickoff()
print(f"Final Output: {final_output}")
print("Final State:")
print(flow.state)