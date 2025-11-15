from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
from metro_service import MetroService

app = FastAPI(
    title="Istanbul Metro API",
    description="API for Istanbul Metro route planning and station information",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize metro service
metro_service = MetroService()

# Request/Response models
class RouteRequest(BaseModel):
    source_id: int
    target_id: int

class RouteResponse(BaseModel):
    path: list
    stations: list
    route_details: list
    total_distance: float
    total_time: float
    num_stations: int


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint - serves the web application"""
    return FileResponse("../frontend/index.html")


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Istanbul Metro API"}


@app.get("/api/stations")
async def get_all_stations():
    """Get all metro stations grouped by line"""
    try:
        stations = metro_service.get_all_stations()
        return {
            "status": "success",
            "data": stations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/lines")
async def get_all_lines():
    """Get all metro lines with their colors"""
    try:
        lines = metro_service.get_all_lines()
        return {
            "status": "success",
            "data": lines
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/station/{station_id}")
async def get_station(station_id: int):
    """Get information about a specific station"""
    try:
        station = metro_service.get_station_by_id(station_id)
        if station is None:
            raise HTTPException(status_code=404, detail="Station not found")
        return {
            "status": "success",
            "data": station
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/search")
async def search_stations(q: str):
    """Search stations by name"""
    try:
        if not q or len(q) < 2:
            raise HTTPException(status_code=400, detail="Query must be at least 2 characters")

        results = metro_service.search_stations(q)
        return {
            "status": "success",
            "data": results,
            "count": len(results)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/route")
async def calculate_route(request: RouteRequest):
    """Calculate shortest route between two stations"""
    try:
        result = metro_service.find_shortest_path(request.source_id, request.target_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="No route found between the specified stations"
            )

        return {
            "status": "success",
            "data": result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats():
    """Get general statistics about the metro network"""
    try:
        stations = metro_service.get_all_stations()
        total_stations = sum(len(line_stations) for line_stations in stations.values())

        return {
            "status": "success",
            "data": {
                "total_lines": len(stations),
                "total_stations": total_stations,
                "lines": {
                    line_name: len(line_stations)
                    for line_name, line_stations in stations.items()
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Mount static files for frontend
if os.path.exists("../frontend/static"):
    app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
