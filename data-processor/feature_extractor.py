#!/usr/bin/env python3
"""
Feature Extractor for Floor Plan Navigator
Extracts features and metadata from floor plan data
"""

import math
from typing import Dict, List, Any, Tuple, Optional

class FeatureExtractor:
    """Extract features and metadata from floor plan data"""
    
    def __init__(self, floor_data: Dict[str, Any]):
        """
        Initialize feature extractor with floor data
        
        Args:
            floor_data (dict): Floor plan data
        """
        self.floor_data = floor_data
        self.rooms = floor_data.get('rooms', [])
        self.doors = floor_data.get('doors', [])
        self.dimensions = floor_data.get('dimensions', {'width': 800, 'height': 600})
    
    def extract_room_features(self, room_id: str) -> Dict[str, Any]:
        """
        Extract features for a specific room
        
        Args:
            room_id (str): Room ID
            
        Returns:
            dict: Room features
        """
        room = self._find_room(room_id)
        if not room:
            return {}
        
        features = {
            'id': room['id'],
            'name': room['name'],
            'area': self._calculate_room_area(room),
            'perimeter': self._calculate_room_perimeter(room),
            'center': room['center'],
            'bounds': room['bounds'],
            'neighbors': self._get_room_neighbors(room_id),
            'door_count': self._count_room_doors(room_id),
            'accessibility_score': self._calculate_accessibility_score(room_id),
            'isolation_score': self._calculate_isolation_score(room_id)
        }
        
        return features
    
    def extract_floor_features(self) -> Dict[str, Any]:
        """
        Extract features for the entire floor
        
        Returns:
            dict: Floor features
        """
        features = {
            'floor_id': self.floor_data.get('floor_id'),
            'floor_number': self.floor_data.get('floor_number'),
            'dimensions': self.dimensions,
            'total_area': self._calculate_total_area(),
            'room_count': len(self.rooms),
            'door_count': len(self.doors),
            'average_room_area': self._calculate_average_room_area(),
            'room_density': self._calculate_room_density(),
            'connectivity_score': self._calculate_connectivity_score(),
            'accessibility_metrics': self._calculate_accessibility_metrics(),
            'room_distribution': self._analyze_room_distribution(),
            'door_distribution': self._analyze_door_distribution()
        }
        
        return features
    
    def extract_path_features(self, path: List[str]) -> Dict[str, Any]:
        """
        Extract features for a path
        
        Args:
            path (list): List of room IDs in the path
            
        Returns:
            dict: Path features
        """
        if not path or len(path) < 2:
            return {}
        
        features = {
            'length': len(path),
            'total_distance': self._calculate_path_distance(path),
            'efficiency': self._calculate_path_efficiency(path),
            'complexity': self._calculate_path_complexity(path),
            'accessibility': self._calculate_path_accessibility(path),
            'rooms': [self.extract_room_features(room_id) for room_id in path],
            'transitions': self._analyze_path_transitions(path)
        }
        
        return features
    
    def _find_room(self, room_id: str) -> Optional[Dict[str, Any]]:
        """Find room by ID"""
        for room in self.rooms:
            if room['id'] == room_id:
                return room
        return None
    
    def _calculate_room_area(self, room: Dict[str, Any]) -> float:
        """Calculate room area"""
        bounds = room.get('bounds', {})
        width = bounds.get('width', 0)
        height = bounds.get('height', 0)
        return width * height
    
    def _calculate_room_perimeter(self, room: Dict[str, Any]) -> float:
        """Calculate room perimeter"""
        bounds = room.get('bounds', {})
        width = bounds.get('width', 0)
        height = bounds.get('height', 0)
        return 2 * (width + height)
    
    def _get_room_neighbors(self, room_id: str) -> List[str]:
        """Get neighboring rooms"""
        neighbors = []
        for door in self.doors:
            if room_id in door.get('connects', []):
                for connected_room in door['connects']:
                    if connected_room != room_id and connected_room not in neighbors:
                        neighbors.append(connected_room)
        return neighbors
    
    def _count_room_doors(self, room_id: str) -> int:
        """Count doors connected to a room"""
        count = 0
        for door in self.doors:
            if room_id in door.get('connects', []):
                count += 1
        return count
    
    def _calculate_accessibility_score(self, room_id: str) -> float:
        """Calculate room accessibility score (0-1)"""
        neighbors = self._get_room_neighbors(room_id)
        door_count = self._count_room_doors(room_id)
        
        # Base score on number of connections
        base_score = min(door_count / 4.0, 1.0)  # Normalize to 0-1
        
        # Bonus for being near center
        room = self._find_room(room_id)
        if room:
            center_x = self.dimensions['width'] / 2
            center_y = self.dimensions['height'] / 2
            distance_from_center = math.sqrt(
                (room['center']['x'] - center_x) ** 2 + 
                (room['center']['y'] - center_y) ** 2
            )
            max_distance = math.sqrt(center_x ** 2 + center_y ** 2)
            center_bonus = 1.0 - (distance_from_center / max_distance)
            base_score += center_bonus * 0.3
        
        return min(base_score, 1.0)
    
    def _calculate_isolation_score(self, room_id: str) -> float:
        """Calculate room isolation score (0-1, higher = more isolated)"""
        neighbors = self._get_room_neighbors(room_id)
        door_count = self._count_room_doors(room_id)
        
        # More isolated if fewer connections
        isolation = 1.0 - (door_count / 4.0)
        return max(0.0, min(isolation, 1.0))
    
    def _calculate_total_area(self) -> float:
        """Calculate total floor area"""
        total = 0
        for room in self.rooms:
            total += self._calculate_room_area(room)
        return total
    
    def _calculate_average_room_area(self) -> float:
        """Calculate average room area"""
        if not self.rooms:
            return 0
        return self._calculate_total_area() / len(self.rooms)
    
    def _calculate_room_density(self) -> float:
        """Calculate room density (rooms per unit area)"""
        total_area = self.dimensions['width'] * self.dimensions['height']
        return len(self.rooms) / total_area if total_area > 0 else 0
    
    def _calculate_connectivity_score(self) -> float:
        """Calculate overall floor connectivity score"""
        if not self.rooms:
            return 0
        
        total_connections = 0
        for room in self.rooms:
            total_connections += self._count_room_doors(room['id'])
        
        # Normalize by number of rooms
        max_possible_connections = len(self.rooms) * (len(self.rooms) - 1)
        return total_connections / max_possible_connections if max_possible_connections > 0 else 0
    
    def _calculate_accessibility_metrics(self) -> Dict[str, float]:
        """Calculate accessibility metrics for the floor"""
        if not self.rooms:
            return {}
        
        accessibility_scores = []
        for room in self.rooms:
            score = self._calculate_accessibility_score(room['id'])
            accessibility_scores.append(score)
        
        return {
            'average_accessibility': sum(accessibility_scores) / len(accessibility_scores),
            'min_accessibility': min(accessibility_scores),
            'max_accessibility': max(accessibility_scores),
            'accessibility_variance': self._calculate_variance(accessibility_scores)
        }
    
    def _analyze_room_distribution(self) -> Dict[str, Any]:
        """Analyze room distribution across the floor"""
        if not self.rooms:
            return {}
        
        x_coords = [room['center']['x'] for room in self.rooms]
        y_coords = [room['center']['y'] for room in self.rooms]
        
        return {
            'x_range': [min(x_coords), max(x_coords)],
            'y_range': [min(y_coords), max(y_coords)],
            'x_center': sum(x_coords) / len(x_coords),
            'y_center': sum(y_coords) / len(y_coords),
            'x_variance': self._calculate_variance(x_coords),
            'y_variance': self._calculate_variance(y_coords)
        }
    
    def _analyze_door_distribution(self) -> Dict[str, Any]:
        """Analyze door distribution across the floor"""
        if not self.doors:
            return {}
        
        x_coords = [door['position']['x'] for door in self.doors]
        y_coords = [door['position']['y'] for door in self.doors]
        
        return {
            'x_range': [min(x_coords), max(x_coords)],
            'y_range': [min(y_coords), max(y_coords)],
            'x_center': sum(x_coords) / len(x_coords),
            'y_center': sum(y_coords) / len(y_coords),
            'x_variance': self._calculate_variance(x_coords),
            'y_variance': self._calculate_variance(y_coords)
        }
    
    def _calculate_path_distance(self, path: List[str]) -> float:
        """Calculate total distance for a path"""
        if len(path) < 2:
            return 0
        
        total_distance = 0
        for i in range(len(path) - 1):
            room1 = self._find_room(path[i])
            room2 = self._find_room(path[i + 1])
            
            if room1 and room2:
                distance = math.sqrt(
                    (room1['center']['x'] - room2['center']['x']) ** 2 +
                    (room1['center']['y'] - room2['center']['y']) ** 2
                )
                total_distance += distance
        
        return total_distance
    
    def _calculate_path_efficiency(self, path: List[str]) -> float:
        """Calculate path efficiency (straight-line distance / actual distance)"""
        if len(path) < 2:
            return 1.0
        
        start_room = self._find_room(path[0])
        end_room = self._find_room(path[-1])
        
        if not start_room or not end_room:
            return 0.0
        
        straight_line_distance = math.sqrt(
            (start_room['center']['x'] - end_room['center']['x']) ** 2 +
            (start_room['center']['y'] - end_room['center']['y']) ** 2
        )
        
        actual_distance = self._calculate_path_distance(path)
        
        return straight_line_distance / actual_distance if actual_distance > 0 else 0.0
    
    def _calculate_path_complexity(self, path: List[str]) -> float:
        """Calculate path complexity (number of turns / path length)"""
        if len(path) < 3:
            return 0.0
        
        # Count direction changes
        direction_changes = 0
        for i in range(1, len(path) - 1):
            room1 = self._find_room(path[i - 1])
            room2 = self._find_room(path[i])
            room3 = self._find_room(path[i + 1])
            
            if room1 and room2 and room3:
                # Calculate angles
                angle1 = math.atan2(
                    room2['center']['y'] - room1['center']['y'],
                    room2['center']['x'] - room1['center']['x']
                )
                angle2 = math.atan2(
                    room3['center']['y'] - room2['center']['y'],
                    room3['center']['x'] - room2['center']['x']
                )
                
                # Check for significant direction change
                angle_diff = abs(angle1 - angle2)
                if angle_diff > math.pi / 4:  # 45 degrees
                    direction_changes += 1
        
        return direction_changes / (len(path) - 2) if len(path) > 2 else 0.0
    
    def _calculate_path_accessibility(self, path: List[str]) -> float:
        """Calculate average accessibility score for path rooms"""
        if not path:
            return 0.0
        
        scores = []
        for room_id in path:
            score = self._calculate_accessibility_score(room_id)
            scores.append(score)
        
        return sum(scores) / len(scores)
    
    def _analyze_path_transitions(self, path: List[str]) -> List[Dict[str, Any]]:
        """Analyze transitions between rooms in path"""
        transitions = []
        
        for i in range(len(path) - 1):
            room1_id = path[i]
            room2_id = path[i + 1]
            
            room1 = self._find_room(room1_id)
            room2 = self._find_room(room2_id)
            
            if room1 and room2:
                distance = math.sqrt(
                    (room1['center']['x'] - room2['center']['x']) ** 2 +
                    (room1['center']['y'] - room2['center']['y']) ** 2
                )
                
                # Find connecting door
                connecting_door = None
                for door in self.doors:
                    if room1_id in door.get('connects', []) and room2_id in door.get('connects', []):
                        connecting_door = door
                        break
                
                transitions.append({
                    'from_room': room1_id,
                    'to_room': room2_id,
                    'distance': distance,
                    'door_id': connecting_door['id'] if connecting_door else None,
                    'door_position': connecting_door['position'] if connecting_door else None
                })
        
        return transitions
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of a list of values"""
        if not values:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance

# Example usage and testing
if __name__ == "__main__":
    # Test with sample data
    sample_data = {
        "floor_id": "test_floor",
        "floor_number": 1,
        "dimensions": {"width": 800, "height": 600},
        "rooms": [
            {
                "id": "101",
                "name": "Room 101",
                "center": {"x": 100, "y": 100},
                "bounds": {"x": 50, "y": 50, "width": 100, "height": 100}
            },
            {
                "id": "102",
                "name": "Room 102",
                "center": {"x": 300, "y": 100},
                "bounds": {"x": 250, "y": 50, "width": 100, "height": 100}
            }
        ],
        "doors": [
            {
                "id": "d1",
                "position": {"x": 200, "y": 100},
                "connects": ["101", "102"]
            }
        ]
    }
    
    extractor = FeatureExtractor(sample_data)
    
    # Test room features
    room_features = extractor.extract_room_features("101")
    print(f"Room 101 features: {room_features}")
    
    # Test floor features
    floor_features = extractor.extract_floor_features()
    print(f"Floor features: {floor_features}")
    
    # Test path features
    path_features = extractor.extract_path_features(["101", "102"])
    print(f"Path features: {path_features}")
