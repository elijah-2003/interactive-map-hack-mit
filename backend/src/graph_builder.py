class GraphBuilder:
    def __init__(self, json_data):
        self.json_data = json_data

    def build_graph(self):
        import networkx as nx
        
        graph = nx.Graph()
        nodes = self.json_data['floor_plan']['nodes']
        edges = self.json_data['floor_plan']['edges']

        for node_id, node_info in nodes.items():
            graph.add_node(node_id, **node_info)

        for edge in edges:
            graph.add_edge(edge['from'], edge['to'], weight=edge['distance'])

        return graph

    @staticmethod
    def load_json(file_path):
        import json
        
        with open(file_path, 'r') as file:
            return json.load(file)