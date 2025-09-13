#!/usr/bin/env python3
"""
Pathfinder for Floor Plan Navigator
Implements pathfinding algorithms for navigation between rooms
"""

import networkx as nx
import math

class PathFinder:
    def __init__(self, graph):
        """
        Initialize pathfinder with a graph
        
        Args:
            graph (networkx.Graph): Graph representation of the floor plan
        """
        self.graph = graph
        self.algorithm = 'dijkstra'  # Default algorithm
        
    def find_path(self, start_room, end_room, algorithm='dijkstra'):
        """
        Find path between two rooms
        
        Args:
            start_room (str): Starting room ID
            end_room (str): Destination room ID
            algorithm (str): Pathfinding algorithm ('dijkstra', 'astar', 'bfs')
            
        Returns:
            dict: Path result with success status, path, and distance
        """
        if not self.graph.has_node(start_room):
            return {
                'success': False,
                'error': f'Starting room {start_room} not found',
                'path': [],
                'distance': 0
            }
        
        if not self.graph.has_node(end_room):
            return {
                'success': False,
                'error': f'Destination room {end_room} not found',
                'path': [],
                'distance': 0
            }
        
        if start_room == end_room:
            return {
                'success': True,
                'path': [start_room],
                'distance': 0
            }
        
        try:
            if algorithm == 'dijkstra':
                return self._find_path_dijkstra(start_room, end_room)
            elif algorithm == 'astar':
                return self._find_path_astar(start_room, end_room)
            elif algorithm == 'bfs':
                return self._find_path_bfs(start_room, end_room)
            else:
                return {
                    'success': False,
                    'error': f'Unknown algorithm: {algorithm}',
                    'path': [],
                    'distance': 0
                }
        except nx.NetworkXNoPath:
            return {
                'success': False,
                'error': f'No path found between {start_room} and {end_room}',
                'path': [],
                'distance': 0
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Pathfinding error: {str(e)}',
                'path': [],
                'distance': 0
            }
    
    def _find_path_dijkstra(self, start_room, end_room):
        """Find path using Dijkstra's algorithm"""
        try:
            path = nx.shortest_path(self.graph, start_room, end_room, weight='weight')
            distance = nx.shortest_path_length(self.graph, start_room, end_room, weight='weight')
            
            return {
                'success': True,
                'path': path,
                'distance': distance
            }
        except nx.NetworkXNoPath:
            raise
    
    def _find_path_astar(self, start_room, end_room):
        """Find path using A* algorithm"""
        try:
            # Define heuristic function (straight-line distance)
            def heuristic(u, v):
                if u not in self.graph.nodes or v not in self.graph.nodes:
                    return 0
                
                pos_u = self.graph.nodes[u].get('center', {'x': 0, 'y': 0})
                pos_v = self.graph.nodes[v].get('center', {'x': 0, 'y': 0})
                
                dx = pos_u['x'] - pos_v['x']
                dy = pos_u['y'] - pos_v['y']
                return math.sqrt(dx*dx + dy*dy)
            
            path = nx.astar_path(self.graph, start_room, end_room, heuristic=heuristic, weight='weight')
            distance = nx.astar_path_length(self.graph, start_room, end_room, heuristic=heuristic, weight='weight')
            
            return {
                'success': True,
                'path': path,
                'distance': distance
            }
        except nx.NetworkXNoPath:
            raise
    
    def _find_path_bfs(self, start_room, end_room):
        """Find path using Breadth-First Search"""
        try:
            path = nx.shortest_path(self.graph, start_room, end_room)
            distance = len(path) - 1  # Number of steps
            
            return {
                'success': True,
                'path': path,
                'distance': distance
            }
        except nx.NetworkXNoPath:
            raise
    
    def find_all_paths(self, start_room, end_room, max_paths=5):
        """
        Find multiple paths between two rooms
        
        Args:
            start_room (str): Starting room ID
            end_room (str): Destination room ID
            max_paths (int): Maximum number of paths to return
            
        Returns:
            list: List of path results
        """
        if not self.graph.has_node(start_room) or not self.graph.has_node(end_room):
            return []
        
        try:
            # Find all simple paths
            all_paths = list(nx.all_simple_paths(self.graph, start_room, end_room, cutoff=10))
            
            # Sort by length and take top paths
            all_paths.sort(key=len)
            top_paths = all_paths[:max_paths]
            
            results = []
            for path in top_paths:
                distance = self._calculate_path_distance(path)
                results.append({
                    'success': True,
                    'path': path,
                    'distance': distance,
                    'steps': len(path) - 1
                })
            
            return results
        except Exception as e:
            return []
    
    def _calculate_path_distance(self, path):
        """Calculate total distance for a path"""
        if len(path) < 2:
            return 0
        
        total_distance = 0
        for i in range(len(path) - 1):
            if self.graph.has_edge(path[i], path[i+1]):
                edge_data = self.graph[path[i]][path[i+1]]
                total_distance += edge_data.get('weight', 1)
        
        return total_distance
    
    def get_room_neighbors(self, room_id):
        """
        Get neighboring rooms
        
        Args:
            room_id (str): Room ID
            
        Returns:
            list: List of neighboring room IDs
        """
        if not self.graph.has_node(room_id):
            return []
        
        return list(self.graph.neighbors(room_id))
    
    def get_shortest_distance(self, start_room, end_room):
        """
        Get shortest distance between two rooms without returning the path
        
        Args:
            start_room (str): Starting room ID
            end_room (str): Destination room ID
            
        Returns:
            float: Shortest distance, or -1 if no path exists
        """
        try:
            return nx.shortest_path_length(self.graph, start_room, end_room, weight='weight')
        except nx.NetworkXNoPath:
            return -1
    
    def is_connected(self, room1, room2):
        """
        Check if two rooms are connected
        
        Args:
            room1 (str): First room ID
            room2 (str): Second room ID
            
        Returns:
            bool: True if rooms are connected
        """
        return self.graph.has_edge(room1, room2)
    
    def get_graph_info(self):
        """
        Get information about the graph
        
        Returns:
            dict: Graph information
        """
        return {
            'nodes': self.graph.number_of_nodes(),
            'edges': self.graph.number_of_edges(),
            'is_connected': nx.is_connected(self.graph),
            'density': nx.density(self.graph),
            'average_clustering': nx.average_clustering(self.graph)
        }

# Example usage and testing
if __name__ == "__main__":
    # Create a simple test graph
    import networkx as nx
    
    G = nx.Graph()
    G.add_edge('A', 'B', weight=1)
    G.add_edge('B', 'C', weight=2)
    G.add_edge('C', 'D', weight=1)
    G.add_edge('A', 'D', weight=4)
    
    pathfinder = PathFinder(G)
    
    # Test pathfinding
    result = pathfinder.find_path('A', 'D')
    print(f"Path from A to D: {result}")
    
    # Test multiple algorithms
    for algo in ['dijkstra', 'astar', 'bfs']:
        result = pathfinder.find_path('A', 'D', algorithm=algo)
        print(f"{algo.upper()}: {result}")
