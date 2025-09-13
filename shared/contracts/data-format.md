# Floor Plan Data Format Specification

This document defines the standard data format for floor plan information used by the Floor Plan Navigator system.

## Overview

The floor plan data is stored in JSON format and contains information about rooms, doors, and their spatial relationships within a building floor.

## Data Structure

### Root Object

```json
{
  "floor_id": "string",
  "floor_number": "number",
  "dimensions": {
    "width": "number",
    "height": "number"
  },
  "rooms": ["array of room objects"],
  "doors": ["array of door objects"]
}
```

### Room Object

Each room represents a navigable space within the floor plan.

```json
{
  "id": "string",           // Unique identifier (e.g., "101", "conference_a")
  "name": "string",         // Human-readable name (e.g., "Conference Room A")
  "center": {               // Center point coordinates
    "x": "number",
    "y": "number"
  },
  "bounds": {               // Bounding rectangle
    "x": "number",          // Left edge
    "y": "number",          // Top edge
    "width": "number",      // Width in pixels/units
    "height": "number"      // Height in pixels/units
  }
}
```

### Door Object

Each door represents a connection between two rooms.

```json
{
  "id": "string",           // Unique identifier (e.g., "d1", "door_101_102")
  "position": {             // Door position coordinates
    "x": "number",
    "y": "number"
  },
  "connects": ["array of exactly 2 room IDs"]  // e.g., ["101", "102"]
}
```

## Coordinate System

- **Origin**: Top-left corner (0, 0)
- **X-axis**: Increases from left to right
- **Y-axis**: Increases from top to bottom
- **Units**: Pixels or arbitrary units (must be consistent)

## Validation Rules

### Required Fields

- `floor_id`: Must be a non-empty string
- `floor_number`: Must be a positive integer
- `dimensions`: Must contain width and height > 0
- `rooms`: Must be an array (can be empty)
- `doors`: Must be an array (can be empty)

### Room Validation

- `id`: Must be unique within the floor
- `name`: Must be a non-empty string
- `center`: Must have valid x, y coordinates
- `bounds`: Must have valid x, y, width, height values
- `bounds.width` and `bounds.height` must be > 0

### Door Validation

- `id`: Must be unique within the floor
- `position`: Must have valid x, y coordinates
- `connects`: Must contain exactly 2 room IDs
- Both room IDs in `connects` must exist in the rooms array

## Example Data

```json
{
  "floor_id": "building_a_floor_1",
  "floor_number": 1,
  "dimensions": {"width": 800, "height": 600},
  "rooms": [
    {
      "id": "101",
      "name": "Conference Room A",
      "center": {"x": 100, "y": 150},
      "bounds": {"x": 50, "y": 100, "width": 100, "height": 100}
    },
    {
      "id": "102",
      "name": "Office 102",
      "center": {"x": 250, "y": 150},
      "bounds": {"x": 200, "y": 100, "width": 100, "height": 100}
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

## Extensions

### Optional Fields

Additional fields may be added to room and door objects as needed:

```json
{
  "id": "101",
  "name": "Conference Room A",
  "center": {"x": 100, "y": 150},
  "bounds": {"x": 50, "y": 100, "width": 100, "height": 100},
  "capacity": 12,                    // Optional: room capacity
  "room_type": "conference",         // Optional: room type
  "accessibility": true,             // Optional: accessibility features
  "amenities": ["projector", "whiteboard"]  // Optional: room amenities
}
```

### Metadata

Additional metadata may be added at the root level:

```json
{
  "floor_id": "building_a_floor_1",
  "floor_number": 1,
  "dimensions": {"width": 800, "height": 600},
  "rooms": [...],
  "doors": [...],
  "metadata": {                      // Optional: additional metadata
    "building_name": "Main Building",
    "last_updated": "2024-01-15T10:30:00Z",
    "version": "1.0.0"
  }
}
```

## File Naming Convention

Floor plan data files should follow this naming pattern:

- Format: `{building_id}_floor_{floor_number}.json`
- Examples:
  - `building_a_floor_1.json`
  - `main_building_floor_2.json`
  - `office_tower_floor_10.json`

## Version History

- **v1.0.0** (2024-01-15): Initial specification
  - Basic room and door structure
  - Coordinate system definition
  - Validation rules
