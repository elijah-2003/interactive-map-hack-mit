import networkx as nx
class JohnsonPathfinder:
    def __init__(self, graph):
        self.graph = graph

    def find_shortest_path(self, start_room, end_room):
        """Find the shortest path between two rooms using Johnson's algorithm."""
        # Step 1: Add a new node to the graph
        self.graph.add_node('source')

        # Step 2: Connect the new node to all other nodes with zero-weight edges
        for node in self.graph.nodes:
            if node != 'source':
                self.graph.add_edge('source', node, weight=0)

        # Step 3: Run Bellman-Ford algorithm from the new node
        try:
            h = nx.single_source_bellman_ford_path_length(self.graph, 'source')
        except nx.NetworkXUnbounded:
            raise ValueError("Graph contains a negative-weight cycle")

        # Step 4: Reweight the edges
        for u, v, data in self.graph.edges(data=True):
            data['weight'] += h[u] - h[v]

        # Step 5: Remove the source node
        self.graph.remove_node('source')

        # Step 6: Use Dijkstra's algorithm to find the shortest path
        try:
            path = nx.shortest_path(self.graph, start_room, end_room, weight='weight')
            distance = nx.shortest_path_length(self.graph, start_room, end_room, weight='weight')
            return {
                'success': True,
                'path': path,
                'distance': distance
            }
        except nx.NetworkXNoPath:
            return {
                'success': False,
                'error': f'No path found between {start_room} and {end_room}',
                'path': [],
                'distance': 0
            }