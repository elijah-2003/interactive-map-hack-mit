// Configuration and mock data for the Floor Plan Navigator
const CONFIG = {
    // Canvas settings
    CANVAS_WIDTH: 800,
    CANVAS_HEIGHT: 600,
    
    // Colors
    COLORS: {
        ROOM: '#3498db',
        ROOM_HOVER: '#2980b9',
        ROOM_SELECTED: '#e74c3c',
        ROOM_PATH: '#f39c12',
        DOOR: '#2c3e50',
        CORRIDOR: '#95a5a6',
        PATH: '#e74c3c',
        PATH_ANIMATED: '#e67e22',
        TEXT: '#2c3e50',
        BACKGROUND: '#fafafa',
        GRID: '#ecf0f1'
    },
    
    // Room styling
    ROOM: {
        WIDTH: 100,
        HEIGHT: 100,
        BORDER_WIDTH: 2,
        CORNER_RADIUS: 8
    },
    
    // Door styling
    DOOR: {
        WIDTH: 4,
        HEIGHT: 20
    },
    
    // Path styling
    PATH: {
        WIDTH: 4,
        DASH_LENGTH: 10,
        DASH_GAP: 5,
        ANIMATION_SPEED: 2
    },
    
    // Animation settings
    ANIMATION: {
        DURATION: 2000,
        EASING: 'ease-in-out'
    }
};

// Mock floor data for testing without backend
const MOCK_FLOOR_DATA = {
    floor_id: "building_a_floor_1",
    floor_number: 1,
    dimensions: { width: 800, height: 600 },
    rooms: [
        {
            id: "101",
            name: "Conference Room A",
            center: { x: 100, y: 150 },
            bounds: { x: 50, y: 100, width: 100, height: 100 }
        },
        {
            id: "102",
            name: "Office 102",
            center: { x: 250, y: 150 },
            bounds: { x: 200, y: 100, width: 100, height: 100 }
        },
        {
            id: "103",
            name: "Office 103",
            center: { x: 400, y: 150 },
            bounds: { x: 350, y: 100, width: 100, height: 100 }
        },
        {
            id: "104",
            name: "Meeting Room B",
            center: { x: 550, y: 150 },
            bounds: { x: 500, y: 100, width: 100, height: 100 }
        },
        {
            id: "105",
            name: "Cafeteria",
            center: { x: 700, y: 150 },
            bounds: { x: 650, y: 100, width: 100, height: 100 }
        }
    ],
    doors: [
        {
            id: "d1",
            position: { x: 150, y: 150 },
            connects: ["101", "102"]
        },
        {
            id: "d2",
            position: { x: 300, y: 150 },
            connects: ["102", "103"]
        },
        {
            id: "d3",
            position: { x: 450, y: 150 },
            connects: ["103", "104"]
        },
        {
            id: "d4",
            position: { x: 600, y: 150 },
            connects: ["104", "105"]
        }
    ]
};

// Mock path data for testing
const MOCK_PATH_DATA = {
    path: ["101", "102", "103", "104", "105"],
    directions: [
        "Start at Conference Room A",
        "Exit through door to Office 102",
        "Continue through door to Office 103",
        "Proceed through door to Meeting Room B",
        "Final destination: Cafeteria"
    ],
    distance: 400,
    estimated_time: "2 minutes"
};

// API Configuration
const API_CONFIG = {
    BASE_URL: 'http://localhost:5000/api',
    TIMEOUT: 5000,
    RETRY_ATTEMPTS: 3
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CONFIG, MOCK_FLOOR_DATA, MOCK_PATH_DATA, API_CONFIG };
}
