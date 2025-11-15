# 🚇 Istanbul Metro Web Application

A modern, interactive web application for planning routes on the Istanbul Metro system. Find the fastest path between stations with real-time visualization, route animations, and approximate travel time calculations.

![Istanbul Metro](https://img.shields.io/badge/Istanbul-Metro-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-teal)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow)

## ✨ Features

- 🗺️ **Interactive Map**: Visual representation of all Istanbul Metro lines and stations using Leaflet.js
- 🎯 **Route Planning**: Find the shortest path between any two stations
- ⏱️ **Time Calculation**: Get approximate travel time based on distance and average metro speed
- 🎬 **Route Animation**: Animated train movement showing your journey station by station
- 📊 **Detailed Route Info**: See distance, time, and line changes for each segment
- 🎨 **Beautiful UI**: Modern, responsive design that works on desktop and mobile
- 🔍 **Station Search**: Click stations on the map to select start/end points

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation & Running

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Istanbul-Metro-API
   ```

2. **Run the application**
   ```bash
   ./start.sh
   ```

   Or manually:
   ```bash
   pip install -r requirements.txt
   cd backend
   python3 main.py
   ```

3. **Open your browser**
   ```
   http://localhost:8000
   ```

That's it! The application should now be running.

## 📁 Project Structure

```
Istanbul-Metro-API/
├── backend/
│   ├── main.py              # FastAPI server and API endpoints
│   └── metro_service.py     # Metro logic and graph operations
├── frontend/
│   ├── index.html           # Main HTML page
│   └── static/
│       ├── css/
│       │   └── style.css    # Styling
│       └── js/
│           └── app.js       # Frontend JavaScript logic
├── src/
│   └── main.py             # Original desktop visualization script
├── requirements.txt         # Python dependencies
├── start.sh                # Quick start script
└── README.md
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **NetworkX**: Graph algorithms for route calculation
- **Requests**: HTTP library for fetching metro data from Istanbul Municipality API

### Frontend
- **Leaflet.js**: Interactive map visualization
- **Vanilla JavaScript**: No framework dependencies
- **CSS3**: Modern styling with animations

## 📡 API Endpoints

### `GET /api/stations`
Get all metro stations grouped by line

**Response:**
```json
{
  "status": "success",
  "data": {
    "M1": [...],
    "M2": [...],
    ...
  }
}
```

### `GET /api/lines`
Get all metro lines with their colors

**Response:**
```json
{
  "status": "success",
  "data": {
    "M1": "#E63946",
    "M2": "#F77F00",
    ...
  }
}
```

### `POST /api/route`
Calculate shortest route between two stations

**Request:**
```json
{
  "source_id": 212,
  "target_id": 301
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "path": [212, 213, 214, ...],
    "stations": [...],
    "route_details": [...],
    "total_distance": 25.5,
    "total_time": 45.2,
    "num_stations": 15
  }
}
```

### `GET /api/station/{station_id}`
Get information about a specific station

### `GET /api/search?q={query}`
Search stations by name

### `GET /api/stats`
Get network statistics

## 🎮 How to Use

1. **Select Start Station**: Click on any station on the map and select "Set as Start"
2. **Select End Station**: Click on another station and select "Set as End"
3. **Find Route**: Click the "Find Route" button
4. **View Details**: See the route details including distance, time, and transfers
5. **Animate**: Click "Animate Route" to see a train moving along your route
6. **Clear**: Use "Clear Route" to start over

## 📝 Notes

- The application fetches real-time station data from the Istanbul Municipality API
- Some tram lines and the new Istanbul Airport Metro may not be included
- Travel time is calculated based on an average speed of 40 km/h with 1-minute stops
- The route finding algorithm uses Dijkstra's shortest path

## 🔧 Development

### Running in Development Mode

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Original Desktop Version

The original matplotlib-based desktop visualization is still available:

```bash
python src/main.py
```

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Istanbul Metropolitan Municipality for providing the Metro API
- OpenStreetMap contributors for map tiles
- Leaflet.js for the amazing mapping library

