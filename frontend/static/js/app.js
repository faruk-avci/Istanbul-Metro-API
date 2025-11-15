// Istanbul Metro Route Planner - Main Application
class MetroApp {
    constructor() {
        this.map = null;
        this.stations = {};
        this.lines = {};
        this.markers = {};
        this.selectedStart = null;
        this.selectedEnd = null;
        this.currentRoute = null;
        this.routeLayer = null;
        this.trainMarker = null;
        this.animationInterval = null;

        this.API_BASE = window.location.origin;
    }

    async init() {
        try {
            // Initialize map
            this.initMap();

            // Load data from API
            await this.loadLines();
            await this.loadStations();

            // Setup event listeners
            this.setupEventListeners();

            // Hide loading spinner
            document.getElementById('loading').classList.add('hidden');
        } catch (error) {
            console.error('Error initializing app:', error);
            alert('Failed to load metro data. Please refresh the page.');
        }
    }

    initMap() {
        // Initialize Leaflet map centered on Istanbul
        this.map = L.map('map').setView([41.0082, 28.9784], 11);

        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(this.map);

        // Create layer for route visualization
        this.routeLayer = L.layerGroup().addTo(this.map);
    }

    async loadLines() {
        const response = await fetch(`${this.API_BASE}/api/lines`);
        const data = await response.json();
        this.lines = data.data;

        // Populate legend
        this.renderLegend();
    }

    async loadStations() {
        const response = await fetch(`${this.API_BASE}/api/stations`);
        const data = await response.json();
        this.stations = data.data;

        // Add markers to map
        this.renderStations();
    }

    renderLegend() {
        const legendContainer = document.getElementById('line-legend');
        legendContainer.innerHTML = '';

        for (const [lineName, color] of Object.entries(this.lines)) {
            const lineItem = document.createElement('div');
            lineItem.className = 'line-item';
            lineItem.innerHTML = `
                <div class="line-color" style="background-color: ${color}"></div>
                <span class="line-name">${lineName}</span>
            `;
            legendContainer.appendChild(lineItem);
        }
    }

    renderStations() {
        for (const [lineName, stationList] of Object.entries(this.stations)) {
            const lineColor = this.lines[lineName] || '#000000';

            stationList.forEach((station, index) => {
                if (!station.latitude || !station.longitude) return;

                const lat = parseFloat(station.latitude);
                const lng = parseFloat(station.longitude);

                // Create custom marker
                const markerIcon = L.divIcon({
                    className: 'station-marker',
                    html: `<div class="station-marker" style="background-color: ${lineColor}"></div>`,
                    iconSize: [12, 12],
                    iconAnchor: [6, 6]
                });

                const marker = L.marker([lat, lng], { icon: markerIcon })
                    .addTo(this.map);

                // Create popup
                const popupContent = `
                    <div class="station-popup">
                        <h4>${station.name}</h4>
                        <p><strong>Line:</strong> ${lineName}</p>
                        <p><strong>ID:</strong> ${station.id}</p>
                        <button onclick="app.selectStation(${station.id}, '${station.name}', 'start')">
                            Set as Start
                        </button>
                        <button onclick="app.selectStation(${station.id}, '${station.name}', 'end')">
                            Set as End
                        </button>
                    </div>
                `;
                marker.bindPopup(popupContent);

                // Store marker reference
                this.markers[station.id] = {
                    marker: marker,
                    station: station,
                    line: lineName
                };

                // Draw line between consecutive stations
                if (index > 0) {
                    const prevStation = stationList[index - 1];
                    if (prevStation.latitude && prevStation.longitude) {
                        const prevLat = parseFloat(prevStation.latitude);
                        const prevLng = parseFloat(prevStation.longitude);

                        L.polyline(
                            [[prevLat, prevLng], [lat, lng]],
                            {
                                color: lineColor,
                                weight: 3,
                                opacity: 0.6
                            }
                        ).addTo(this.map);
                    }
                }
            });
        }
    }

    selectStation(stationId, stationName, type) {
        if (type === 'start') {
            this.selectedStart = { id: stationId, name: stationName };
            document.getElementById('start-station').value = stationName;
            document.getElementById('start-station').classList.add('selected');

            // Update marker
            this.updateMarkerStyle(stationId, 'start');
        } else if (type === 'end') {
            this.selectedEnd = { id: stationId, name: stationName };
            document.getElementById('end-station').value = stationName;
            document.getElementById('end-station').classList.add('selected');

            // Update marker
            this.updateMarkerStyle(stationId, 'end');
        }

        // Enable find route button if both stations selected
        const findBtn = document.getElementById('find-route');
        findBtn.disabled = !(this.selectedStart && this.selectedEnd);

        // Close popup
        this.map.closePopup();
    }

    updateMarkerStyle(stationId, type) {
        if (this.markers[stationId]) {
            const markerData = this.markers[stationId];
            const lineColor = this.lines[markerData.line];

            let className = 'station-marker selected';
            if (type === 'start') className += ' start';
            if (type === 'end') className += ' end';

            const newIcon = L.divIcon({
                className: className,
                html: `<div class="${className}" style="background-color: ${type === 'start' ? '#27ae60' : type === 'end' ? '#e74c3c' : lineColor}"></div>`,
                iconSize: [16, 16],
                iconAnchor: [8, 8]
            });

            markerData.marker.setIcon(newIcon);
        }
    }

    resetMarkerStyle(stationId) {
        if (this.markers[stationId]) {
            const markerData = this.markers[stationId];
            const lineColor = this.lines[markerData.line];

            const defaultIcon = L.divIcon({
                className: 'station-marker',
                html: `<div class="station-marker" style="background-color: ${lineColor}"></div>`,
                iconSize: [12, 12],
                iconAnchor: [6, 6]
            });

            markerData.marker.setIcon(defaultIcon);
        }
    }

    async findRoute() {
        if (!this.selectedStart || !this.selectedEnd) {
            alert('Please select both start and end stations');
            return;
        }

        try {
            const response = await fetch(`${this.API_BASE}/api/route`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    source_id: this.selectedStart.id,
                    target_id: this.selectedEnd.id
                })
            });

            const data = await response.json();

            if (data.status === 'success') {
                this.currentRoute = data.data;
                this.displayRoute();
            } else {
                alert('No route found between selected stations');
            }
        } catch (error) {
            console.error('Error finding route:', error);
            alert('Failed to calculate route. Please try again.');
        }
    }

    displayRoute() {
        if (!this.currentRoute) return;

        // Clear previous route
        this.routeLayer.clearLayers();

        // Show route info panel
        document.getElementById('route-info').style.display = 'block';

        // Update stats
        document.getElementById('total-distance').textContent =
            `${this.currentRoute.total_distance} km`;
        document.getElementById('total-time').textContent =
            `${this.currentRoute.total_time} min`;
        document.getElementById('num-stations').textContent =
            this.currentRoute.num_stations;

        // Draw route on map
        const coordinates = this.currentRoute.stations.map(station => [
            parseFloat(station.latitude),
            parseFloat(station.longitude)
        ]);

        // Draw highlighted route
        const routeLine = L.polyline(coordinates, {
            color: '#ff6b6b',
            weight: 5,
            opacity: 0.8,
            dashArray: '10, 5',
            lineJoin: 'round'
        }).addTo(this.routeLayer);

        // Fit map to route bounds
        this.map.fitBounds(routeLine.getBounds(), { padding: [50, 50] });

        // Display route steps
        this.displayRouteSteps();
    }

    displayRouteSteps() {
        const stepsContainer = document.getElementById('route-steps');
        stepsContainer.innerHTML = '';

        this.currentRoute.route_details.forEach((step, index) => {
            const lineColor = this.lines[step.line] || '#000000';

            const stepDiv = document.createElement('div');
            stepDiv.className = 'route-step';
            stepDiv.innerHTML = `
                <div class="route-step-icon" style="background-color: ${lineColor}; color: white;">
                    ${index + 1}
                </div>
                <div class="route-step-content">
                    <div class="route-step-stations">
                        ${step.from_name} → ${step.to_name}
                    </div>
                    <div class="route-step-info">
                        Line ${step.line} • ${step.distance} km • ${step.time} min
                    </div>
                </div>
            `;
            stepsContainer.appendChild(stepDiv);
        });
    }

    animateRoute() {
        if (!this.currentRoute) return;

        // Clear any existing animation
        this.stopAnimation();

        const stations = this.currentRoute.stations;
        let currentIndex = 0;

        // Create animated train marker
        const trainIcon = L.divIcon({
            className: 'train-marker',
            html: '<div class="train-marker">🚇</div>',
            iconSize: [20, 20],
            iconAnchor: [10, 10]
        });

        this.trainMarker = L.marker(
            [parseFloat(stations[0].latitude), parseFloat(stations[0].longitude)],
            { icon: trainIcon }
        ).addTo(this.routeLayer);

        // Animate train movement
        this.animationInterval = setInterval(() => {
            currentIndex++;

            if (currentIndex >= stations.length) {
                // Animation complete
                this.stopAnimation();
                return;
            }

            const station = stations[currentIndex];
            const newLatLng = L.latLng(
                parseFloat(station.latitude),
                parseFloat(station.longitude)
            );

            // Smooth animation to next station
            this.trainMarker.setLatLng(newLatLng);

            // Pan map to follow train
            this.map.panTo(newLatLng);
        }, 1000); // Move to next station every second
    }

    stopAnimation() {
        if (this.animationInterval) {
            clearInterval(this.animationInterval);
            this.animationInterval = null;
        }

        if (this.trainMarker) {
            this.routeLayer.removeLayer(this.trainMarker);
            this.trainMarker = null;
        }
    }

    clearRoute() {
        // Clear route visualization
        this.routeLayer.clearLayers();
        this.currentRoute = null;

        // Hide route info
        document.getElementById('route-info').style.display = 'none';

        // Stop animation
        this.stopAnimation();
    }

    clearSelection(type) {
        if (type === 'start') {
            if (this.selectedStart) {
                this.resetMarkerStyle(this.selectedStart.id);
                this.selectedStart = null;
            }
            document.getElementById('start-station').value = '';
            document.getElementById('start-station').classList.remove('selected');
        } else if (type === 'end') {
            if (this.selectedEnd) {
                this.resetMarkerStyle(this.selectedEnd.id);
                this.selectedEnd = null;
            }
            document.getElementById('end-station').value = '';
            document.getElementById('end-station').classList.remove('selected');
        }

        // Disable find route button if either station is cleared
        const findBtn = document.getElementById('find-route');
        findBtn.disabled = !(this.selectedStart && this.selectedEnd);
    }

    swapStations() {
        const temp = this.selectedStart;
        this.selectedStart = this.selectedEnd;
        this.selectedEnd = temp;

        // Update UI
        const startInput = document.getElementById('start-station');
        const endInput = document.getElementById('end-station');

        const tempValue = startInput.value;
        startInput.value = endInput.value;
        endInput.value = tempValue;

        // Update marker styles
        if (this.selectedStart) {
            this.updateMarkerStyle(this.selectedStart.id, 'start');
        }
        if (this.selectedEnd) {
            this.updateMarkerStyle(this.selectedEnd.id, 'end');
        }
    }

    setupEventListeners() {
        // Find route button
        document.getElementById('find-route').addEventListener('click', () => {
            this.findRoute();
        });

        // Clear buttons
        document.getElementById('clear-start').addEventListener('click', () => {
            this.clearSelection('start');
        });

        document.getElementById('clear-end').addEventListener('click', () => {
            this.clearSelection('end');
        });

        // Swap button
        document.getElementById('swap-stations').addEventListener('click', () => {
            this.swapStations();
        });

        // Animate route button
        document.getElementById('animate-route').addEventListener('click', () => {
            this.animateRoute();
        });

        // Clear route button
        document.getElementById('clear-route').addEventListener('click', () => {
            this.clearRoute();
        });
    }
}

// Initialize app when DOM is ready
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new MetroApp();
    app.init();
});
