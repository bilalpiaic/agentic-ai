from crewai.flow.flow import Flow, listen, or_, start

class DataAggregationFlow(Flow):

    @start()
    def fetch_data_source_1(self):
        # Simulate data fetching
        data1 = {"source": "API 1", "value": 100}
        self.state["data1"] = data1
        return data1

    @start()
    def fetch_data_source_2(self):
        # Simulate data fetching
        data2 = {"source": "API 2", "value": 200}
        self.state["data2"] = data2
        return data2

    @listen(or_(fetch_data_source_1, fetch_data_source_2))
    def process_data(self, data1=None, data2=None):
        aggregated_data = []
        if data1:
            aggregated_data.append(data1)
        if data2:
            aggregated_data.append(data2)
        self.state["aggregated_data"] = aggregated_data
        return aggregated_data

    @listen(process_data)
    def logger(self, aggregated_data):
        print(f"Aggregated Data: {aggregated_data}")

flow = DataAggregationFlow()
flow.kickoff()
