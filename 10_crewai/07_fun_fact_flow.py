from crewai.flow.flow import Flow, listen, start
from dotenv import load_dotenv


from litellm import completion


class ExampleFlow(Flow):
    # model = "gpt-4o-mini"
    # model = "gemini/gemini-pro"
    model = "gemini/gemini-1.5-flash"

    @start()
    def generate_city(self):
        print("Starting flow")
        # Each flow state automatically gets a unique ID


        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": "Return the name of a random city in the world.",
                },
            ],
        )

        random_city = response["choices"][0]["message"]["content"]
        # Store the city in our state
        self.state["city"] = random_city

        print(f"Random City: {random_city}")

        return random_city

    @listen(generate_city)
    def generate_fun_fact(self, random_city):
        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"Tell me a fun fact about {random_city}",
                },
            ],
        )

        fun_fact = response["choices"][0]["message"]["content"]
        # Store the fun fact in our state
        self.state["fun_fact"] = fun_fact
        return fun_fact



flow = ExampleFlow()
result = flow.kickoff()

print(f"Generated fun fact: {result}")