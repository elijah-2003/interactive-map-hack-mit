#!/usr/bin/env python3
"""
Graph Builder for Floor Plan Navigator
Converts floor plan data into a graph structure for pathfinding
"""

import networkx as nx
import math

class GraphBuilder:
    def __init__(self, floor_data):
        """
        Initialize graph builder with floor data
        
        Args:
            floor_data (dict): Floor plan data containing rooms and doors
        """
        self.floor_data = floor_data
        self.graph = nx.Graph()
        
    def build_graph(self):
        """
        Build graph from floor data
        
        Returns:
            networkx.Graph: Graph representation of the floor plan
        """
        if not self.floor_data:
            raise ValueError("No floor data provided")
        
        # Clear existing graph
        self.graph.clear()
        
        # Add room nodes
        self._add_room_nodes()
        
        # Add door connections
        self._add_door_connections()
        
        # Add corridor connections
        self._add_corridor_connections()
        
        return self.graph
    
    def _add_room_nodes(self):
        """Add room nodes to the graph"""
        if 'rooms' not in self.floor_data:
            return
        
        for room in self.floor_data['rooms']:
            self.graph.add_node(
                room['id'],
                type='room',
                name=room['name'],
                center=room['center'],
                bounds=room['bounds']
            )
    
    def _add_door_connections(self):
        """Add connections through doors"""
        if 'doors' not in self.floor_data:
            return
        
        for door in self.floor_data['doors']:
            if 'connects' in door and len(door['connects']) == 2:
                room1_id = door['connects'][0]
                room2_id = door['connects'][1]
                
                # Calculate distance between room centers
                distance = self._calculate_distance(
                    door['position'],
                    door['position']  # Door position is the connection point
                )
                
                # Add edge with weight (distance)
                self.graph.add_edge(
                    room1_id,
                    room2_id,
                    type='door',
                    weight=distance,
                    door_id=door['id'],
                    position=door['position']
                )
    
    def _add_corridor_connections(self):
        """Add corridor connections between nearby rooms"""
        if 'rooms' not in self.floor_data:
            return
        
        rooms = self.floor_data['rooms']
        
        # Check for potential corridor connections
        for i, room1 in enumerate(rooms):
            for room2 in rooms[i+1:]:
                # Skip if already connected by door
                if self.graph.has_edge(room1['id'], room2['id']):
                    continue
                
                # Check if rooms are close enough for corridor connection
                distance = self._calculate_distance(room1['center'], room2['center'])
                
                # Add corridor connection if rooms are reasonably close
                if distance < 200:  # Adjust threshold as needed
                    self.graph.add_edge(
                        room1['id'],
                        room2['id'],
                        type='corridor',
                        weight=distance * 1.2,  # Corridors are slightly longer
                        position=None
                    )
    
    def _calculate_distance(self, pos1, pos2):
        """Calculate Euclidean distance between two positions"""
        dx = pos1['x'] - pos2['x']
        dy = pos1['y'] - pos2['y']
        return math.sqrt(dx*dx + dy*dy)
    
    def get_room_connections(self, room_id):
        """
        Get all rooms connected to a given room
        
        Args:
            room_id (str): ID of the room
            
        Returns:
            list: List of connected room IDs
        """
        if not self.graph.has_node(room_id):
            return []
        
        return list(self.graph.neighbors(room_id))
    
    def get_connection_type(self, room1_id, room2_id):
        """
        Get the type of connection between two rooms
        
        Args:
            room1_id (str): First room ID
            room2_id (str): Second room ID
            
        Returns:
            str: Connection type ('door', 'corridor', or None)
        """
        if not self.graph.has_edge(room1_id, room2_id):
            return None
        
        return self.graph[room1_id][room2_id].get('type')
    
    def get_graph_stats(self):
        """
        Get statistics about the built graph
        
        Returns:
            dict: Graph statistics
        """
        return {
            'nodes': self.graph.number_of_nodes(),
            'edges': self.graph.number_of_edges(),
            'is_connected': nx.is_connected(self.graph),
            'density': nx.density(self.graph),
            'average_clustering': nx.average_clustering(self.graph)
        }
    
    def visualize_graph(self):
        """
        Create a simple text visualization of the graph
        
        Returns:
            str: Text representation of the graph
        """
        if not self.graph.nodes():
            return "Empty graph"
        
        lines = ["Graph Structure:"]
        lines.append(f"Nodes: {self.graph.number_of_nodes()}")
        lines.append(f"Edges: {self.graph.number_of_edges()}")
        lines.append("")
        
        for node in sorted(self.graph.nodes()):
            neighbors = list(self.graph.neighbors(node))
            lines.append(f"{node}: {neighbors}")
        
        return "\n".join(lines)

# Example usage and testing
if __name__ == "__main__":
    # Test with sample data
    sample_data = {
        "floor_id": "test_floor",
        "rooms": [
            {"id": "101", "name": "Room 101", "center": {"x": 100, "y": 100}, "bounds": {"x": 50, "y": 50, "width": 100, "height": 100}},
            {"id": "102", "name": "Room 102", "center": {"x": 300, "y": 100}, "bounds": {"x": 250, "y": 50, "width": 100, "height": 100}}
        ],
        "doors": [
            {"id": "d1", "position": {"x": 200, "y": 100}, "connects": ["101", "102"]}
        ]
    }
    
    builder = GraphBuilder(sample_data)
    graph = builder.build_graph()
    
    print("Graph built successfully!")
    print(builder.visualize_graph())
    print(f"Stats: {builder.get_graph_stats()}")
