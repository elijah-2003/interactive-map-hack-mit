#!/usr/bin/env python3
"""
Parser for Floor Plan Navigator
Handles parsing of various floor plan data formats
"""

import json
import xml.etree.ElementTree as ET
import csv
import os
from typing import Dict, List, Any, Optional

class FloorPlanParser:
    """Parser for different floor plan data formats"""
    
    def __init__(self):
        self.supported_formats = ['json', 'xml', 'csv']
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse floor plan data from file
        
        Args:
            file_path (str): Path to the floor plan file
            
        Returns:
            dict: Parsed floor plan data
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.json':
            return self.parse_json(file_path)
        elif file_extension == '.xml':
            return self.parse_xml(file_path)
        elif file_extension == '.csv':
            return self.parse_csv(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def parse_json(self, file_path: str) -> Dict[str, Any]:
        """Parse JSON floor plan data"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate required fields
            self._validate_floor_data(data)
            
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
        except Exception as e:
            raise ValueError(f"Error parsing JSON: {e}")
    
    def parse_xml(self, file_path: str) -> Dict[str, Any]:
        """Parse XML floor plan data"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Convert XML to dictionary
            data = self._xml_to_dict(root)
            
            # Validate required fields
            self._validate_floor_data(data)
            
            return data
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML format: {e}")
        except Exception as e:
            raise ValueError(f"Error parsing XML: {e}")
    
    def parse_csv(self, file_path: str) -> Dict[str, Any]:
        """Parse CSV floor plan data"""
        try:
            data = {
                'floor_id': 'csv_floor',
                'floor_number': 1,
                'dimensions': {'width': 800, 'height': 600},
                'rooms': [],
                'doors': []
            }
            
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    if row.get('type') == 'room':
                        room = {
                            'id': row['id'],
                            'name': row.get('name', row['id']),
                            'center': {
                                'x': float(row.get('x', 0)),
                                'y': float(row.get('y', 0))
                            },
                            'bounds': {
                                'x': float(row.get('x', 0)) - 50,
                                'y': float(row.get('y', 0)) - 50,
                                'width': float(row.get('width', 100)),
                                'height': float(row.get('height', 100))
                            }
                        }
                        data['rooms'].append(room)
                    elif row.get('type') == 'door':
                        door = {
                            'id': row['id'],
                            'position': {
                                'x': float(row.get('x', 0)),
                                'y': float(row.get('y', 0))
                            },
                            'connects': row.get('connects', '').split(',')
                        }
                        data['doors'].append(door)
            
            # Validate required fields
            self._validate_floor_data(data)
            
            return data
        except Exception as e:
            raise ValueError(f"Error parsing CSV: {e}")
    
    def _xml_to_dict(self, element: ET.Element) -> Dict[str, Any]:
        """Convert XML element to dictionary"""
        result = {}
        
        # Add attributes
        if element.attrib:
            result.update(element.attrib)
        
        # Add text content if no children
        if len(element) == 0 and element.text and element.text.strip():
            return element.text.strip()
        
        # Process children
        for child in element:
            child_data = self._xml_to_dict(child)
            
            if child.tag in result:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        return result
    
    def _validate_floor_data(self, data: Dict[str, Any]) -> None:
        """Validate floor plan data structure"""
        required_fields = ['floor_id', 'rooms']
        
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate rooms
        if not isinstance(data['rooms'], list):
            raise ValueError("Rooms must be a list")
        
        for i, room in enumerate(data['rooms']):
            if not isinstance(room, dict):
                raise ValueError(f"Room {i} must be a dictionary")
            
            required_room_fields = ['id', 'center']
            for field in required_room_fields:
                if field not in room:
                    raise ValueError(f"Room {i} missing required field: {field}")
            
            # Validate center coordinates
            if not isinstance(room['center'], dict):
                raise ValueError(f"Room {i} center must be a dictionary")
            
            if 'x' not in room['center'] or 'y' not in room['center']:
                raise ValueError(f"Room {i} center must have x and y coordinates")
        
        # Validate doors if present
        if 'doors' in data:
            if not isinstance(data['doors'], list):
                raise ValueError("Doors must be a list")
            
            for i, door in enumerate(data['doors']):
                if not isinstance(door, dict):
                    raise ValueError(f"Door {i} must be a dictionary")
                
                required_door_fields = ['id', 'position', 'connects']
                for field in required_door_fields:
                    if field not in door:
                        raise ValueError(f"Door {i} missing required field: {field}")
    
    def export_json(self, data: Dict[str, Any], output_path: str) -> None:
        """Export data to JSON format"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise ValueError(f"Error exporting JSON: {e}")
    
    def export_xml(self, data: Dict[str, Any], output_path: str) -> None:
        """Export data to XML format"""
        try:
            root = ET.Element('floor_plan')
            root.set('id', data.get('floor_id', 'unknown'))
            root.set('floor_number', str(data.get('floor_number', 1)))
            
            # Add dimensions
            if 'dimensions' in data:
                dims = ET.SubElement(root, 'dimensions')
                dims.set('width', str(data['dimensions']['width']))
                dims.set('height', str(data['dimensions']['height']))
            
            # Add rooms
            rooms_elem = ET.SubElement(root, 'rooms')
            for room in data.get('rooms', []):
                room_elem = ET.SubElement(rooms_elem, 'room')
                room_elem.set('id', room['id'])
                room_elem.set('name', room.get('name', room['id']))
                
                center = ET.SubElement(room_elem, 'center')
                center.set('x', str(room['center']['x']))
                center.set('y', str(room['center']['y']))
                
                if 'bounds' in room:
                    bounds = ET.SubElement(room_elem, 'bounds')
                    bounds.set('x', str(room['bounds']['x']))
                    bounds.set('y', str(room['bounds']['y']))
                    bounds.set('width', str(room['bounds']['width']))
                    bounds.set('height', str(room['bounds']['height']))
            
            # Add doors
            doors_elem = ET.SubElement(root, 'doors')
            for door in data.get('doors', []):
                door_elem = ET.SubElement(doors_elem, 'door')
                door_elem.set('id', door['id'])
                
                position = ET.SubElement(door_elem, 'position')
                position.set('x', str(door['position']['x']))
                position.set('y', str(door['position']['y']))
                
                connects = ET.SubElement(door_elem, 'connects')
                for room_id in door['connects']:
                    room_ref = ET.SubElement(connects, 'room')
                    room_ref.set('id', room_id)
            
            # Write to file
            tree = ET.ElementTree(root)
            tree.write(output_path, encoding='utf-8', xml_declaration=True)
        except Exception as e:
            raise ValueError(f"Error exporting XML: {e}")

# Example usage and testing
if __name__ == "__main__":
    parser = FloorPlanParser()
    
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
            }
        ],
        "doors": []
    }
    
    # Test JSON export
    parser.export_json(sample_data, "test_output.json")
    print("JSON export successful")
    
    # Test JSON import
    parsed_data = parser.parse_json("test_output.json")
    print("JSON import successful")
    print(f"Parsed data: {parsed_data['floor_id']}")
    
    # Clean up
    os.remove("test_output.json")
