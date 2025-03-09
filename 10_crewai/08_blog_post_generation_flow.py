from crewai.flow.flow import Flow, listen, start
from litellm import completion

class BlogPostCreationFlow(Flow):
    model = "gpt-4o-mini"
    

    @start()
    def select_topic(self):
        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": "Suggest a trending technology topic for a blog post.",
                },
            ],
        )
        topic = response["choices"][0]["message"]["content"]
        self.state["topic"] = topic
        return topic

    @listen(select_topic)
    def create_outline(self, topic):
        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"Create a detailed outline for a blog post on '{topic}'.",
                },
            ],
        )
        outline = response["choices"][0]["message"]["content"]
        self.state["outline"] = outline
        return outline

    @listen(create_outline)
    def write_draft(self, outline):
        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"Write a comprehensive draft based on the following outline:\n{outline}",
                },
            ],
        )
        draft = response["choices"][0]["message"]["content"]
        self.state["draft"] = draft
        return draft

    @listen(write_draft)
    def edit_draft(self, draft):
        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"Edit the following draft for clarity, grammar, and style:\n{draft}",
                },
            ],
        )
        edited_draft = response["choices"][0]["message"]["content"]
        self.state["edited_draft"] = edited_draft
        return edited_draft

flow = BlogPostCreationFlow()
result = flow.kickoff()
print(f"Final Edited Blog Post:\n{result}")
