# Floor Plan Navigator API Specification

This document defines the REST API endpoints for the Floor Plan Navigator system.

## Base URL

```
http://localhost:5000/api
```

## Authentication

Currently no authentication is required. All endpoints are publicly accessible.

## Response Format

All responses are in JSON format with the following structure:

### Success Response

```json
{
  "status": "success",
  "data": { ... },
  "message": "Optional success message"
}
```

### Error Response

```json
{
  "status": "error",
  "error": "Error message",
  "code": "ERROR_CODE"
}
```

## Endpoints

### 1. Health Check

Check if the API is running and healthy.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "message": "Floor Plan Navigator API is running",
  "floor_data_loaded": true,
  "pathfinder_ready": true
}
```

**Status Codes:**
- `200 OK`: API is healthy
- `500 Internal Server Error`: API is not healthy

---

### 2. Get Available Floors

Retrieve a list of available floors.

**Endpoint:** `GET /api/floors`

**Response:**
```json
[
  {
    "id": "building_a_floor_1",
    "name": "Building A - Floor 1",
    "floor_number": 1
  }
]
```

**Status Codes:**
- `200 OK`: Success
- `500 Internal Server Error`: Server error

---

### 3. Get Floor Data

Retrieve detailed floor plan data for a specific floor.

**Endpoint:** `GET /api/floor/{floor_id}`

**Parameters:**
- `floor_id` (path): Unique identifier for the floor

**Response:**
```json
{
  "floor_id": "building_a_floor_1",
  "floor_number": 1,
  "dimensions": {
    "width": 800,
    "height": 600
  },
  "rooms": [
    {
      "id": "101",
      "name": "Conference Room A",
      "center": {"x": 100, "y": 150},
      "bounds": {"x": 50, "y": 100, "width": 100, "height": 100}
    }
  ],
  "doors": [
    {
      "id": "d1",
      "position": {"x": 150, "y": 150},
      "connects": ["101", "102"]
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Floor not found
- `500 Internal Server Error`: Server error

---

### 4. Find Navigation Path

Find the optimal path between two rooms.

**Endpoint:** `POST /api/navigate`

**Request Body:**
```json
{
  "from_room": "101",
  "to_room": "105",
  "floor_id": "building_a_floor_1"
}
```

**Parameters:**
- `from_room` (required): Starting room ID
- `to_room` (required): Destination room ID
- `floor_id` (optional): Floor ID (defaults to first available floor)

**Response:**
```json
{
  "path": ["101", "102", "103", "104", "105"],
  "directions": [
    "Start at Conference Room A",
    "Exit through door to Office 102",
    "Continue through door to Office 103",
    "Proceed through door to Meeting Room B",
    "Arrive at Cafeteria"
  ],
  "distance": 400,
  "estimated_time": "2 minutes"
}
```

**Status Codes:**
- `200 OK`: Path found successfully
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Room not found or no path exists
- `500 Internal Server Error`: Server error

## Error Codes

| Code | Description |
|------|-------------|
| `INVALID_ROOM` | Room ID does not exist |
| `NO_PATH` | No path exists between the specified rooms |
| `INVALID_FLOOR` | Floor ID does not exist |
| `MISSING_PARAMETER` | Required parameter is missing |
| `INVALID_REQUEST` | Request format is invalid |

## Rate Limiting

Currently no rate limiting is implemented. In production, consider implementing rate limiting to prevent abuse.

## CORS

Cross-Origin Resource Sharing (CORS) is enabled for all origins. This allows the frontend to make requests from any domain.

## Example Usage

### JavaScript (Frontend)

```javascript
// Check API health
const healthResponse = await fetch('http://localhost:5000/api/health');
const health = await healthResponse.json();

// Get available floors
const floorsResponse = await fetch('http://localhost:5000/api/floors');
const floors = await floorsResponse.json();

// Get floor data
const floorResponse = await fetch('http://localhost:5000/api/floor/building_a_floor_1');
const floorData = await floorResponse.json();

// Find path
const pathResponse = await fetch('http://localhost:5000/api/navigate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    from_room: '101',
    to_room: '105',
    floor_id: 'building_a_floor_1'
  })
});
const pathData = await pathResponse.json();
```

### Python (Backend/Testing)

```python
import requests

# Check API health
health = requests.get('http://localhost:5000/api/health').json()

# Get available floors
floors = requests.get('http://localhost:5000/api/floors').json()

# Get floor data
floor_data = requests.get('http://localhost:5000/api/floor/building_a_floor_1').json()

# Find path
path_data = requests.post('http://localhost:5000/api/navigate', json={
    'from_room': '101',
    'to_room': '105',
    'floor_id': 'building_a_floor_1'
}).json()
```

### cURL

```bash
# Check API health
curl -X GET http://localhost:5000/api/health

# Get available floors
curl -X GET http://localhost:5000/api/floors

# Get floor data
curl -X GET http://localhost:5000/api/floor/building_a_floor_1

# Find path
curl -X POST http://localhost:5000/api/navigate \
  -H "Content-Type: application/json" \
  -d '{"from_room": "101", "to_room": "105", "floor_id": "building_a_floor_1"}'
```

## Future Enhancements

### Planned Features

1. **Multiple Pathfinding Algorithms**
   - A* algorithm
   - Breadth-First Search
   - Custom algorithms for specific use cases

2. **Path Optimization**
   - Shortest distance
   - Fewest turns
   - Accessibility considerations

3. **Real-time Updates**
   - WebSocket support for live updates
   - Room availability status
   - Dynamic path recalculation

4. **Analytics**
   - Path usage statistics
   - Popular routes
   - Traffic patterns

5. **Authentication & Authorization**
   - User authentication
   - Role-based access control
   - API key management

### Version History

- **v1.0.0** (2024-01-15): Initial API specification
  - Basic health check
  - Floor data retrieval
  - Pathfinding functionality
