#!/usr/bin/env python3
"""
Flask API server for Floor Plan Navigator
Provides endpoints for floor data and pathfinding
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import sys
from pathfinder import PathFinder
from graph_builder import GraphBuilder

# Add parent directory to path for shared imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables for data and pathfinder
floor_data = None
pathfinder = None
graph_builder = None

def load_floor_data():
    """Load floor data from JSON file"""
    global floor_data, pathfinder, graph_builder
    
    try:
        # Load floor data
        data_path = os.path.join(os.path.dirname(__file__), '..', 'shared', 'sample-data', 'floor1.json')
        with open(data_path, 'r') as f:
            floor_data = json.load(f)
        
        # Build graph and initialize pathfinder
        graph_builder = GraphBuilder(floor_data)
        graph = graph_builder.build_graph()
        pathfinder = PathFinder(graph)
        
        print(f"✅ Loaded floor data: {floor_data['floor_id']}")
        print(f"✅ Built graph with {len(graph.nodes)} nodes and {len(graph.edges)} edges")
        
    except FileNotFoundError:
        print(f"❌ Floor data file not found: {data_path}")
        floor_data = None
    except Exception as e:
        print(f"❌ Error loading floor data: {e}")
        floor_data = None

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Floor Plan Navigator API is running',
        'floor_data_loaded': floor_data is not None,
        'pathfinder_ready': pathfinder is not None
    })

@app.route('/api/floors', methods=['GET'])
def get_floors():
    """Get list of available floors"""
    if not floor_data:
        return jsonify({'error': 'Floor data not loaded'}), 500
    
    return jsonify([{
        'id': floor_data['floor_id'],
        'name': f"Building A - Floor {floor_data['floor_number']}",
        'floor_number': floor_data['floor_number']
    }])

@app.route('/api/floor/<floor_id>', methods=['GET'])
def get_floor_data(floor_id):
    """Get floor data by ID"""
    if not floor_data:
        return jsonify({'error': 'Floor data not loaded'}), 500
    
    if floor_data['floor_id'] != floor_id:
        return jsonify({'error': 'Floor not found'}), 404
    
    return jsonify(floor_data)

@app.route('/api/navigate', methods=['POST'])
def navigate():
    """Find path between two rooms"""
    if not pathfinder:
        return jsonify({'error': 'Pathfinder not initialized'}), 500
    
    try:
        data = request.get_json()
        from_room = data.get('from_room')
        to_room = data.get('to_room')
        floor_id = data.get('floor_id')
        
        if not from_room or not to_room:
            return jsonify({'error': 'from_room and to_room are required'}), 400
        
        # Find path
        path_result = pathfinder.find_path(from_room, to_room)
        
        if not path_result['success']:
            return jsonify({
                'error': path_result['error'],
                'path': [],
                'directions': [],
                'distance': 0
            }), 404
        
        # Generate directions
        directions = generate_directions(path_result['path'], floor_data)
        
        return jsonify({
            'path': path_result['path'],
            'directions': directions,
            'distance': path_result['distance'],
            'estimated_time': f"{len(path_result['path'])} minutes"
        })
        
    except Exception as e:
        return jsonify({'error': f'Navigation failed: {str(e)}'}), 500

def generate_directions(path, floor_data):
    """Generate human-readable directions from path"""
    if not path or len(path) < 2:
        return []
    
    directions = []
    rooms = {room['id']: room for room in floor_data['rooms']}
    
    # Start direction
    start_room = rooms.get(path[0])
    if start_room:
        directions.append(f"Start at {start_room['name']}")
    
    # Intermediate directions
    for i in range(1, len(path) - 1):
        current_room = rooms.get(path[i])
        if current_room:
            directions.append(f"Continue to {current_room['name']}")
    
    # End direction
    end_room = rooms.get(path[-1])
    if end_room:
        directions.append(f"Arrive at {end_room['name']}")
    
    return directions

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting Floor Plan Navigator API...")
    
    # Load floor data
    load_floor_data()
    
    if not floor_data:
        print("❌ Failed to load floor data. Server will start but navigation will not work.")
    
    # Start server
    print("🌐 Server starting on http://localhost:5000")
    print("📋 Available endpoints:")
    print("   GET  /api/health")
    print("   GET  /api/floors")
    print("   GET  /api/floor/<floor_id>")
    print("   POST /api/navigate")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
