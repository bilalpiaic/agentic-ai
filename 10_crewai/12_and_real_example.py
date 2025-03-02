from crewai.flow.flow import Flow, listen, and_, start

class ContentModerationFlow(Flow):
    prohibited_keywords = ["spam", "offensive"]

    @start()
    def receive_content(self):
        content = "This is a user-generated comment."
        self.state["content"] = content
        return content

    @listen(receive_content)
    def analyze_sentiment(self, content):
        # Placeholder for sentiment analysis
        sentiment = "positive"  # Assume a function determines this
        self.state["sentiment"] = sentiment
        return sentiment

    @listen(receive_content)
    def check_prohibited_keywords(self, content):
        contains_prohibited = any(keyword in content for keyword in self.prohibited_keywords)
        self.state["contains_prohibited"] = contains_prohibited
        return contains_prohibited

    @listen(and_(analyze_sentiment, check_prohibited_keywords))
    def decide_approval(self):
        if self.state["sentiment"] == "positive" and not self.state["contains_prohibited"]:
            decision = "approved"
        else:
            decision = "flagged for review"
        self.state["decision"] = decision
        return decision

    @listen(decide_approval)
    def logger(self, decision):
        print(f"Content decision: {decision}")

flow = ContentModerationFlow()
flow.kickoff()
