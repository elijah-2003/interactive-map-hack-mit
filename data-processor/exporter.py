#!/usr/bin/env python3
"""
Exporter for Floor Plan Navigator
Handles export of processed floor plan data to various formats
"""

import json
import csv
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

class FloorPlanExporter:
    """Export floor plan data to various formats"""
    
    def __init__(self):
        self.supported_formats = ['json', 'csv', 'txt', 'html']
    
    def export_floor_data(self, data: Dict[str, Any], output_path: str, format: str = 'json') -> None:
        """
        Export floor data to specified format
        
        Args:
            data (dict): Floor plan data
            output_path (str): Output file path
            format (str): Export format ('json', 'csv', 'txt', 'html')
        """
        if format == 'json':
            self._export_json(data, output_path)
        elif format == 'csv':
            self._export_csv(data, output_path)
        elif format == 'txt':
            self._export_txt(data, output_path)
        elif format == 'html':
            self._export_html(data, output_path)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def export_room_features(self, features: List[Dict[str, Any]], output_path: str, format: str = 'json') -> None:
        """
        Export room features to specified format
        
        Args:
            features (list): List of room features
            output_path (str): Output file path
            format (str): Export format
        """
        if format == 'json':
            self._export_json(features, output_path)
        elif format == 'csv':
            self._export_features_csv(features, output_path)
        else:
            raise ValueError(f"Unsupported export format for features: {format}")
    
    def export_path_analysis(self, path_data: Dict[str, Any], output_path: str, format: str = 'json') -> None:
        """
        Export path analysis data
        
        Args:
            path_data (dict): Path analysis data
            output_path (str): Output file path
            format (str): Export format
        """
        if format == 'json':
            self._export_json(path_data, output_path)
        elif format == 'txt':
            self._export_path_txt(path_data, output_path)
        else:
            raise ValueError(f"Unsupported export format for path analysis: {format}")
    
    def _export_json(self, data: Any, output_path: str) -> None:
        """Export data to JSON format"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            raise ValueError(f"Error exporting JSON: {e}")
    
    def _export_csv(self, data: Dict[str, Any], output_path: str) -> None:
        """Export floor data to CSV format"""
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow(['type', 'id', 'name', 'x', 'y', 'width', 'height', 'connects'])
                
                # Write rooms
                for room in data.get('rooms', []):
                    writer.writerow([
                        'room',
                        room['id'],
                        room.get('name', room['id']),
                        room['center']['x'],
                        room['center']['y'],
                        room.get('bounds', {}).get('width', 0),
                        room.get('bounds', {}).get('height', 0),
                        ''
                    ])
                
                # Write doors
                for door in data.get('doors', []):
                    writer.writerow([
                        'door',
                        door['id'],
                        '',
                        door['position']['x'],
                        door['position']['y'],
                        0,
                        0,
                        ','.join(door.get('connects', []))
                    ])
        except Exception as e:
            raise ValueError(f"Error exporting CSV: {e}")
    
    def _export_txt(self, data: Dict[str, Any], output_path: str) -> None:
        """Export floor data to text format"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"Floor Plan Data Export\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*50}\n\n")
                
                # Floor information
                f.write(f"Floor ID: {data.get('floor_id', 'Unknown')}\n")
                f.write(f"Floor Number: {data.get('floor_number', 'Unknown')}\n")
                f.write(f"Dimensions: {data.get('dimensions', {}).get('width', 0)} x {data.get('dimensions', {}).get('height', 0)}\n\n")
                
                # Rooms
                f.write(f"Rooms ({len(data.get('rooms', []))}):\n")
                f.write(f"{'-'*30}\n")
                for room in data.get('rooms', []):
                    f.write(f"ID: {room['id']}\n")
                    f.write(f"Name: {room.get('name', 'N/A')}\n")
                    f.write(f"Center: ({room['center']['x']}, {room['center']['y']})\n")
                    bounds = room.get('bounds', {})
                    f.write(f"Bounds: ({bounds.get('x', 0)}, {bounds.get('y', 0)}) {bounds.get('width', 0)}x{bounds.get('height', 0)}\n")
                    f.write(f"\n")
                
                # Doors
                f.write(f"Doors ({len(data.get('doors', []))}):\n")
                f.write(f"{'-'*30}\n")
                for door in data.get('doors', []):
                    f.write(f"ID: {door['id']}\n")
                    f.write(f"Position: ({door['position']['x']}, {door['position']['y']})\n")
                    f.write(f"Connects: {', '.join(door.get('connects', []))}\n")
                    f.write(f"\n")
        except Exception as e:
            raise ValueError(f"Error exporting TXT: {e}")
    
    def _export_html(self, data: Dict[str, Any], output_path: str) -> None:
        """Export floor data to HTML format"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("<!DOCTYPE html>\n")
                f.write("<html>\n<head>\n")
                f.write("<title>Floor Plan Data Export</title>\n")
                f.write("<style>\n")
                f.write("body { font-family: Arial, sans-serif; margin: 20px; }\n")
                f.write("table { border-collapse: collapse; width: 100%; margin: 20px 0; }\n")
                f.write("th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }\n")
                f.write("th { background-color: #f2f2f2; }\n")
                f.write("h1, h2 { color: #333; }\n")
                f.write("</style>\n")
                f.write("</head>\n<body>\n")
                
                f.write(f"<h1>Floor Plan Data Export</h1>\n")
                f.write(f"<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>\n")
                
                # Floor information
                f.write(f"<h2>Floor Information</h2>\n")
                f.write(f"<p><strong>Floor ID:</strong> {data.get('floor_id', 'Unknown')}</p>\n")
                f.write(f"<p><strong>Floor Number:</strong> {data.get('floor_number', 'Unknown')}</p>\n")
                f.write(f"<p><strong>Dimensions:</strong> {data.get('dimensions', {}).get('width', 0)} x {data.get('dimensions', {}).get('height', 0)}</p>\n")
                
                # Rooms table
                f.write(f"<h2>Rooms ({len(data.get('rooms', []))})</h2>\n")
                f.write("<table>\n")
                f.write("<tr><th>ID</th><th>Name</th><th>Center X</th><th>Center Y</th><th>Width</th><th>Height</th></tr>\n")
                
                for room in data.get('rooms', []):
                    bounds = room.get('bounds', {})
                    f.write(f"<tr>")
                    f.write(f"<td>{room['id']}</td>")
                    f.write(f"<td>{room.get('name', 'N/A')}</td>")
                    f.write(f"<td>{room['center']['x']}</td>")
                    f.write(f"<td>{room['center']['y']}</td>")
                    f.write(f"<td>{bounds.get('width', 0)}</td>")
                    f.write(f"<td>{bounds.get('height', 0)}</td>")
                    f.write(f"</tr>\n")
                
                f.write("</table>\n")
                
                # Doors table
                f.write(f"<h2>Doors ({len(data.get('doors', []))})</h2>\n")
                f.write("<table>\n")
                f.write("<tr><th>ID</th><th>Position X</th><th>Position Y</th><th>Connects</th></tr>\n")
                
                for door in data.get('doors', []):
                    f.write(f"<tr>")
                    f.write(f"<td>{door['id']}</td>")
                    f.write(f"<td>{door['position']['x']}</td>")
                    f.write(f"<td>{door['position']['y']}</td>")
                    f.write(f"<td>{', '.join(door.get('connects', []))}</td>")
                    f.write(f"</tr>\n")
                
                f.write("</table>\n")
                f.write("</body>\n</html>\n")
        except Exception as e:
            raise ValueError(f"Error exporting HTML: {e}")
    
    def _export_features_csv(self, features: List[Dict[str, Any]], output_path: str) -> None:
        """Export room features to CSV format"""
        try:
            if not features:
                return
            
            # Get all possible field names
            all_fields = set()
            for feature in features:
                all_fields.update(feature.keys())
            
            fieldnames = sorted(list(all_fields))
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for feature in features:
                    # Convert complex objects to strings
                    row = {}
                    for key, value in feature.items():
                        if isinstance(value, (dict, list)):
                            row[key] = json.dumps(value)
                        else:
                            row[key] = value
                    writer.writerow(row)
        except Exception as e:
            raise ValueError(f"Error exporting features CSV: {e}")
    
    def _export_path_txt(self, path_data: Dict[str, Any], output_path: str) -> None:
        """Export path analysis to text format"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"Path Analysis Report\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*50}\n\n")
                
                # Path information
                f.write(f"Path Length: {path_data.get('length', 0)} rooms\n")
                f.write(f"Total Distance: {path_data.get('total_distance', 0):.2f} units\n")
                f.write(f"Efficiency: {path_data.get('efficiency', 0):.2f}\n")
                f.write(f"Complexity: {path_data.get('complexity', 0):.2f}\n")
                f.write(f"Accessibility: {path_data.get('accessibility', 0):.2f}\n\n")
                
                # Room details
                f.write(f"Room Details:\n")
                f.write(f"{'-'*30}\n")
                for room in path_data.get('rooms', []):
                    f.write(f"Room {room.get('id', 'Unknown')}:\n")
                    f.write(f"  Name: {room.get('name', 'N/A')}\n")
                    f.write(f"  Area: {room.get('area', 0):.2f}\n")
                    f.write(f"  Accessibility: {room.get('accessibility_score', 0):.2f}\n")
                    f.write(f"  Neighbors: {', '.join(room.get('neighbors', []))}\n")
                    f.write(f"\n")
                
                # Transitions
                f.write(f"Transitions:\n")
                f.write(f"{'-'*30}\n")
                for i, transition in enumerate(path_data.get('transitions', [])):
                    f.write(f"Step {i+1}: {transition.get('from_room', 'Unknown')} -> {transition.get('to_room', 'Unknown')}\n")
                    f.write(f"  Distance: {transition.get('distance', 0):.2f}\n")
                    f.write(f"  Door: {transition.get('door_id', 'N/A')}\n")
                    f.write(f"\n")
        except Exception as e:
            raise ValueError(f"Error exporting path TXT: {e}")
    
    def create_export_summary(self, data: Dict[str, Any], output_path: str) -> None:
        """Create a summary of all exportable data"""
        try:
            summary = {
                'export_info': {
                    'generated': datetime.now().isoformat(),
                    'floor_id': data.get('floor_id'),
                    'floor_number': data.get('floor_number'),
                    'total_rooms': len(data.get('rooms', [])),
                    'total_doors': len(data.get('doors', [])),
                    'dimensions': data.get('dimensions', {})
                },
                'room_summary': self._create_room_summary(data.get('rooms', [])),
                'door_summary': self._create_door_summary(data.get('doors', [])),
                'export_formats': self.supported_formats
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise ValueError(f"Error creating export summary: {e}")
    
    def _create_room_summary(self, rooms: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create summary of room data"""
        if not rooms:
            return {}
        
        areas = []
        for room in rooms:
            bounds = room.get('bounds', {})
            area = bounds.get('width', 0) * bounds.get('height', 0)
            areas.append(area)
        
        return {
            'count': len(rooms),
            'average_area': sum(areas) / len(areas) if areas else 0,
            'min_area': min(areas) if areas else 0,
            'max_area': max(areas) if areas else 0,
            'room_ids': [room['id'] for room in rooms]
        }
    
    def _create_door_summary(self, doors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create summary of door data"""
        if not doors:
            return {}
        
        return {
            'count': len(doors),
            'door_ids': [door['id'] for door in doors],
            'connection_pairs': [door.get('connects', []) for door in doors]
        }

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
            }
        ],
        "doors": []
    }
    
    exporter = FloorPlanExporter()
    
    # Test JSON export
    exporter.export_floor_data(sample_data, "test_export.json", "json")
    print("JSON export successful")
    
    # Test CSV export
    exporter.export_floor_data(sample_data, "test_export.csv", "csv")
    print("CSV export successful")
    
    # Test HTML export
    exporter.export_floor_data(sample_data, "test_export.html", "html")
    print("HTML export successful")
    
    # Clean up
    for file in ["test_export.json", "test_export.csv", "test_export.html"]:
        if os.path.exists(file):
            os.remove(file)
