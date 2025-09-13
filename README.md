# 🏢 Floor Plan Navigator

A complete floor plan navigation system built for a 24-hour hackathon. This project provides an interactive web-based interface for visualizing floor plans and finding optimal paths between rooms.

## 🚀 Features

- **Interactive Floor Plan Visualization**: HTML5 Canvas-based floor plan renderer
- **Pathfinding**: Multiple algorithms (Dijkstra, A*, BFS) for finding optimal routes
- **Real-time Navigation**: Step-by-step directions with visual path highlighting
- **Responsive Design**: Modern, clean UI that works on desktop and mobile
- **Backend API**: Flask-based REST API with CORS support
- **Data Processing**: Tools for parsing and analyzing floor plan data
- **Mock Data Support**: Works offline with built-in sample data

## 🏗️ Project Structure

```
floor-plan-navigator/
├── frontend/                 # Frontend visualization (HTML5 Canvas)
│   ├── index.html           # Main HTML file
│   ├── css/
│   │   └── style.css        # Modern CSS styling
│   ├── js/
│   │   ├── app.js          # Main application logic
│   │   ├── api.js          # API client
│   │   ├── visualizer.js   # Canvas-based floor plan renderer
│   │   └── config.js       # Configuration and mock data
│   └── assets/             # Static assets
├── backend/                 # Backend API (Flask)
│   ├── server.py           # Flask API server
│   ├── graph_builder.py    # Graph construction from floor data
│   ├── pathfinder.py       # Pathfinding algorithms
│   └── requirements.txt    # Python dependencies
├── data-processor/         # Data processing tools
│   ├── parser.py           # Multi-format data parser
│   ├── feature_extractor.py # Feature extraction and analysis
│   └── exporter.py         # Data export utilities
├── shared/                 # Shared resources
│   ├── sample-data/
│   │   └── floor1.json     # Sample floor plan data
│   └── contracts/
│       ├── data-format.md  # Data format specification
│       └── api-spec.md     # API specification
└── docs/                   # Documentation
```

## 🛠️ Technology Stack

### Frontend
- **HTML5 Canvas**: Interactive floor plan visualization
- **Vanilla JavaScript**: No framework dependencies
- **CSS3**: Modern styling with Flexbox and animations
- **Responsive Design**: Mobile-friendly interface

### Backend
- **Python 3.8+**: Core backend language
- **Flask**: Lightweight web framework
- **NetworkX**: Graph algorithms and data structures
- **Flask-CORS**: Cross-origin resource sharing

### Data Processing
- **JSON/XML/CSV**: Multiple input formats supported
- **Feature Extraction**: Room analysis and metrics
- **Export Tools**: Multiple output formats

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd floor-plan-navigator
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Start the backend server**
   ```bash
   python server.py
   ```
   The API will be available at `http://localhost:5000`

4. **Open the frontend**
   - Open `frontend/index.html` in your web browser
   - Or serve it with a local web server:
     ```bash
     cd frontend
     python -m http.server 8000
     ```
     Then visit `http://localhost:8000`

## 📖 Usage

### Basic Navigation

1. **Select Rooms**: Use the dropdown menus to select starting and destination rooms
2. **Find Path**: Click "Find Path" to calculate the optimal route
3. **View Directions**: Step-by-step directions will appear below the map
4. **Clear Path**: Click "Clear" to reset the visualization

### Keyboard Shortcuts

- **Escape**: Clear current path
- **Ctrl+Enter**: Find path between selected rooms

### Offline Mode

The application works offline using mock data when the backend is unavailable. The status indicator shows whether the backend is online or offline.

## 🔧 Configuration

### Frontend Configuration

Edit `frontend/js/config.js` to customize:

- Canvas dimensions
- Color schemes
- Room styling
- Animation settings
- Mock data

### Backend Configuration

Edit `backend/server.py` to modify:

- API endpoints
- CORS settings
- Data loading
- Error handling

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/floors` | List available floors |
| GET | `/api/floor/{floor_id}` | Get floor data |
| POST | `/api/navigate` | Find path between rooms |

### Example API Usage

```javascript
// Find path between rooms
const response = await fetch('http://localhost:5000/api/navigate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    from_room: '101',
    to_room: '105',
    floor_id: 'building_a_floor_1'
  })
});
const pathData = await response.json();
```

## 📁 Data Format

Floor plan data is stored in JSON format with the following structure:

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

## 🧪 Testing

### Frontend Testing

Open the browser developer console to see:
- API communication logs
- Error messages
- Performance metrics

### Backend Testing

```bash
# Test API endpoints
curl http://localhost:5000/api/health
curl http://localhost:5000/api/floors
curl http://localhost:5000/api/floor/building_a_floor_1
```

### Data Processing Testing

```bash
cd data-processor
python parser.py
python feature_extractor.py
python exporter.py
```

## 🚀 Deployment

### Development

1. Start the backend server
2. Open the frontend in a browser
3. Use the application locally

### Production

1. **Backend**: Deploy Flask app to your preferred hosting service
2. **Frontend**: Serve static files through a web server
3. **Database**: Add persistent storage for floor plan data
4. **Security**: Implement authentication and authorization

## 🤝 Team Roles

This project is designed for a 3-person team:

1. **Frontend Developer** (Visualization)
   - HTML5 Canvas implementation
   - User interface design
   - Interactive features

2. **Backend Developer** (Pathfinding)
   - Flask API development
   - Graph algorithms
   - Pathfinding logic

3. **Data Processor** (Structure Parsing)
   - Data format parsing
   - Feature extraction
   - Export utilities

## 🔮 Future Enhancements

- **Multi-floor Support**: Navigate between different floors
- **Real-time Updates**: Live room availability
- **Mobile App**: Native mobile application
- **3D Visualization**: Three-dimensional floor plans
- **Analytics**: Usage statistics and insights
- **Accessibility**: Enhanced accessibility features
- **Internationalization**: Multi-language support

## 📝 License

This project is created for educational purposes during a hackathon. Feel free to use and modify as needed.

## 🐛 Troubleshooting

### Common Issues

1. **Backend not starting**: Check Python version and dependencies
2. **CORS errors**: Ensure Flask-CORS is installed and configured
3. **Canvas not rendering**: Check browser compatibility
4. **Path not found**: Verify room IDs and door connections

### Getting Help

1. Check the browser console for errors
2. Verify API endpoints are responding
3. Ensure data format matches specification
4. Check network connectivity

## 📞 Support

For questions or issues:
1. Check the documentation in `/docs`
2. Review the API specification
3. Examine the sample data format
4. Test with the provided mock data

---

**Happy Navigating! 🗺️**
