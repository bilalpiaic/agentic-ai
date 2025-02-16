# from crewai.flow.flow import Flow, listen, or_, start

# class OrExampleFlow(Flow):

#     @start()
#     def start_method(self):
#         return "Hello from the start method"

#     @listen(start_method)
#     def second_method(self):
#         return "Hello from the second method"

#     @listen(or_(start_method, second_method))
#     def logger(self, result):
#         print(f"Logger: {result}")
    
    
# flow = OrExampleFlow()
# flow.kickoff()

from crewai.flow.flow import Flow, and_, listen, start

class AndExampleFlow(Flow):

    @start()
    def start_method(self):
        self.state["greeting"] = "Hello from the start method"

    @listen(start_method)
    def second_method(self):
        self.state["joke"] = "What do computers eat? Microchips."

    @listen(and_(start_method, second_method))
    def logger(self):
        print("---- Logger ----")
        print(self.state)

flow = AndExampleFlow()
flow.kickoff()