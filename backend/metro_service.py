import requests
import networkx as nx
from typing import Dict, List, Tuple, Optional
import math


class MetroService:
    def __init__(self):
        self.G = nx.Graph()
        self.stations = {
            "M5": [], "M4": [], "M8": [], "MM": [], "M2": [], "M7": [], "M3": [],
            "T1": [], "T5": [], "M1A": [], "M1B": [], "M6": [], "M9": [], "M11": [],
            "T4": [], "F1": [], "F4": []
        }
        self.line_colors = {
            "M5": "#E63946", "M4": "#1D3557", "M8": "#2A9D8F", "MM": "#9D4EDD",
            "M2": "#F77F00", "M7": "#06AED5", "M3": "#8B4513", "T1": "#FF69B4",
            "T5": "#FFD700", "M1A": "#6C757D", "M1B": "#E83283", "M6": "#90EE90",
            "M9": "#008080", "M11": "#4B0082", "T4": "#800000", "F1": "#000080",
            "F4": "#808000"
        }
        self.load_stations()
        self.build_graph()

    def load_stations(self):
        """Load station data from Istanbul Metro API"""
        try:
            response = requests.get(
                "https://api.ibb.gov.tr/MetroIstanbul/api/MetroMobile/V2/GetStations",
                timeout=10
            )

            # Check if response is valid
            if response.status_code == 200 and response.text.strip():
                data = response.json()

                # Parse stations from API
                for station_data in data["Data"]:
                    for key in self.stations:
                        if station_data["LineName"] == key:
                            station = {
                                "name": station_data["Name"],
                                "latitude": station_data["DetailInfo"].get("Latitude", ""),
                                "longitude": station_data["DetailInfo"].get("Longitude", ""),
                                "id": station_data["Id"],
                                "order": station_data["Order"],
                                "line": key
                            }
                            self.stations[key].append(station)
            else:
                print(f"Warning: API returned status {response.status_code}, using manual data only")

            # Apply manual corrections and add Marmaray line
            # This also provides fallback data if API fails
            self._apply_corrections()

        except Exception as e:
            print(f"Warning: Could not fetch from API ({e}), using manual station data")
            # Apply corrections which include full data for some lines
            self._apply_corrections()

    def _apply_corrections(self):
        """Apply manual corrections to station data"""
        # Marmaray (MM) line data
        self.stations["MM"] = [
            {'name': 'GEBZE', 'latitude': '40.784181', 'longitude': '29.3935358', 'id': 301, 'order': 1, 'line': 'MM'},
            {'name': 'DARICA', 'latitude': '40.78982', 'longitude': '29.3895205', 'id': 302, 'order': 2, 'line': 'MM'},
            {'name': 'OSMANGAZI', 'latitude': '40.7986566', 'longitude': '29.3782534', 'id': 303, 'order': 3, 'line': 'MM'},
            {'name': 'GEBZE_TEKNIK_ÜNIVERSITESI', 'latitude': '40.8082463', 'longitude': '29.3594667', 'id': 304, 'order': 4, 'line': 'MM'},
            {'name': 'CAYIROVA', 'latitude': '40.8107955', 'longitude': '29.3465654', 'id': 305, 'order': 5, 'line': 'MM'},
            {'name': 'TUZLA', 'latitude': '40.8290353', 'longitude': '29.3207176', 'id': 306, 'order': 6, 'line': 'MM'},
            {'name': 'ICMELER', 'latitude': '40.8455518', 'longitude': '29.2998963', 'id': 307, 'order': 7, 'line': 'MM'},
            {'name': 'AYDINTEPE', 'latitude': '40.8508856', 'longitude': '29.295064', 'id': 308, 'order': 8, 'line': 'MM'},
            {'name': 'GUZELYALI', 'latitude': '40.8561729', 'longitude': '29.2860626', 'id': 309, 'order': 9, 'line': 'MM'},
            {'name': 'TERSANE', 'latitude': '40.8598315', 'longitude': '29.2747476', 'id': 310, 'order': 10, 'line': 'MM'},
            {'name': 'KAYNARCA', 'latitude': '40.8705039', 'longitude': '29.2558612', 'id': 311, 'order': 11, 'line': 'MM'},
            {'name': 'PENDIK', 'latitude': '40.8806883', 'longitude': '29.2316707', 'id': 312, 'order': 12, 'line': 'MM'},
            {'name': 'YUNUS', 'latitude': '40.8834551', 'longitude': '29.2091668', 'id': 313, 'order': 13, 'line': 'MM'},
            {'name': 'KARTAL', 'latitude': '40.8870486', 'longitude': '29.1851243', 'id': 314, 'order': 14, 'line': 'MM'},
            {'name': 'BASAK', 'latitude': '40.891103', 'longitude': '29.1752967', 'id': 315, 'order': 15, 'line': 'MM'},
            {'name': 'ATALAR', 'latitude': '40.8981152', 'longitude': '29.1674154', 'id': 316, 'order': 16, 'line': 'MM'},
            {'name': 'CEVIZLI', 'latitude': '40.9082929', 'longitude': '29.155834', 'id': 317, 'order': 17, 'line': 'MM'},
            {'name': 'MALTEPE', 'latitude': '40.9198759', 'longitude': '29.1308588', 'id': 318, 'order': 18, 'line': 'MM'},
            {'name': 'SUREYYA_PLAJI', 'latitude': '40.9261565', 'longitude': '29.1197238', 'id': 319, 'order': 19, 'line': 'MM'},
            {'name': 'IDEALTEPE', 'latitude': '40.9383674', 'longitude': '29.1099494', 'id': 320, 'order': 20, 'line': 'MM'},
            {'name': 'KUUCKYALI', 'latitude': '40.9439545', 'longitude': '29.1057246', 'id': 321, 'order': 21, 'line': 'MM'},
            {'name': 'BOSTANCI', 'latitude': '40.95128998347687', 'longitude': '29.097243057130374', 'id': 161, 'order': 22, 'line': 'MM'},
            {'name': 'SUADIYE', 'latitude': '40.9587123', 'longitude': '29.0850411', 'id': 323, 'order': 23, 'line': 'MM'},
            {'name': 'ERENKOY', 'latitude': '40.9703631', 'longitude': '29.0736159', 'id': 324, 'order': 24, 'line': 'MM'},
            {'name': 'GOZTEPE', 'latitude': '40.9782839', 'longitude': '29.0594758', 'id': 325, 'order': 25, 'line': 'MM'},
            {'name': 'FENERYOLU', 'latitude': '40.9767792', 'longitude': '29.0465906', 'id': 326, 'order': 26, 'line': 'MM'},
            {'name': 'SOGUTLUCESME', 'latitude': '40.9925862', 'longitude': '29.0333966', 'id': 327, 'order': 27, 'line': 'MM'},
            {'name': 'AYRILIK_CESMESI', 'latitude': '41.00020434433358', 'longitude': '29.030153258203203', 'id': 2, 'order': 28, 'line': 'MM'},
            {'name': 'USKUDAR', 'latitude': '41.025618259645256', 'longitude': '29.015061927581854', 'id': 122, 'order': 29, 'line': 'MM'},
            {'name': 'SIRKECI', 'latitude': '41.015180', 'longitude': '28.975890', 'id': 330, 'order': 30, 'line': 'MM'},
            {'name': 'YENIKAPI', 'latitude': '41.0055971704', 'longitude': '28.9513306172', 'id': 20, 'order': 31, 'line': 'MM'},
            {'name': 'KAZLICESME', 'latitude': '40.9920031', 'longitude': '28.9166025', 'id': 332, 'order': 32, 'line': 'MM'},
            {'name': 'ZEYTINBURNU', 'latitude': '40.9866357', 'longitude': '28.9045622', 'id': 333, 'order': 33, 'line': 'MM'},
            {'name': 'YENIMAHALLE', 'latitude': '40.9817211', 'longitude': '28.8824225', 'id': 334, 'order': 34, 'line': 'MM'},
            {'name': 'BAKIRKOY', 'latitude': '40.9815344', 'longitude': '28.8734009', 'id': 335, 'order': 35, 'line': 'MM'},
            {'name': 'ATAKOY', 'latitude': '40.9794168', 'longitude': '28.8555328', 'id': 336, 'order': 36, 'line': 'MM'},
            {'name': 'YESILYURT', 'latitude': '40.9630548', 'longitude': '28.830968', 'id': 337, 'order': 37, 'line': 'MM'},
            {'name': 'YESILKOY', 'latitude': '40.9627362', 'longitude': '28.8247946', 'id': 338, 'order': 38, 'line': 'MM'},
            {'name': 'FLORYA_AKVARUM', 'latitude': '40.96556', 'longitude': '28.7983628', 'id': 339, 'order': 39, 'line': 'MM'},
            {'name': 'FLORYA', 'latitude': '40.9715111', 'longitude': '28.790156', 'id': 340, 'order': 40, 'line': 'MM'},
            {'name': 'KUCUKCEKMECE', 'latitude': '40.98784', 'longitude': '28.773917', 'id': 341, 'order': 41, 'line': 'MM'},
            {'name': 'MUSTAFA_KEMAL', 'latitude': '41.0028258', 'longitude': '28.7656428', 'id': 342, 'order': 42, 'line': 'MM'},
            {'name': 'HALKALI', 'latitude': '41.0167685', 'longitude': '28.7682746', 'id': 343, 'order': 43, 'line': 'MM'}
        ]

        # M8 corrections
        if len(self.stations["M8"]) > 10:
            self.stations["M8"][10]["latitude"] = "41.01544045560607"
            self.stations["M8"][10]["longitude"] = "29.16244635386456"
            self.stations["M8"][10]["id"] = 135
        if len(self.stations["M8"]) > 3:
            self.stations["M8"][3]["latitude"] = "40.9748528607554"
            self.stations["M8"][3]["longitude"] = "29.099330474424526"
            self.stations["M8"][3]["id"] = 7

        # M7 corrections
        if len(self.stations["M7"]) > 2:
            self.stations["M7"][2]["latitude"] = "41.0645069127"
            self.stations["M7"][2]["longitude"] = "28.9926697578"
            self.stations["M7"][2]["id"] = 26
        if len(self.stations["M7"]) > 8:
            self.stations["M7"][8]["latitude"] = "41.0799901"
            self.stations["M7"][8]["longitude"] = "28.9352699"
        if len(self.stations["M7"]) > 9:
            self.stations["M7"][9]["latitude"] = "41.0796898"
            self.stations["M7"][9]["longitude"] = "28.9295594"

        # M3 corrections and complete data
        self.stations["M3"] = [
            {'name': 'KAYASEHIR MERKEZ', 'latitude': '41.1183031', 'longitude': '28.7655255', 'id': 240, 'order': 13, 'line': 'M3'},
            {'name': 'TOPLU KONUTLAR', 'latitude': '41.1068062', 'longitude': '28.767267', 'id': 239, 'order': 12, 'line': 'M3'},
            {'name': 'SEHIR HASTANESI', 'latitude': '41.1031843', 'longitude': '28.7762591', 'id': 238, 'order': 11, 'line': 'M3'},
            {'name': 'ONURKENT', 'latitude': '41.1133997', 'longitude': '28.7905842', 'id': 237, 'order': 10, 'line': 'M3'},
            {'name': 'METROKENT', 'latitude': '41.1075899254', 'longitude': '28.8014768347', 'id': 36, 'order': 9, 'line': 'M3'},
            {'name': 'BASAK KONUTLARI', 'latitude': '41.0976705948', 'longitude': '28.7912824671', 'id': 37, 'order': 8, 'line': 'M3'},
            {'name': 'SITELER', 'latitude': '41.0882027223', 'longitude': '28.7965104065', 'id': 38, 'order': 7, 'line': 'M3'},
            {'name': 'TURGUT OZAL', 'latitude': '41.0811852568', 'longitude': '28.7974049311', 'id': 39, 'order': 6, 'line': 'M3'},
            {'name': 'IKITELLI SANAYI', 'latitude': '41.0724333906', 'longitude': '28.8023285305', 'id': 40, 'order': 5, 'line': 'M3'},
            {'name': 'ISTOC', 'latitude': '41.0649996532', 'longitude': '28.8259591715', 'id': 41, 'order': 4, 'line': 'M3'},
            {'name': 'MAHMUTBEY', 'latitude': '41.054312', 'longitude': '28.830612', 'id': 160, 'order': 3, 'line': 'M3'},
            {'name': 'YENIMAHALLE', 'latitude': '41.0403571945', 'longitude': '28.8359378583', 'id': 43, 'order': 2, 'line': 'M3'},
            {'name': 'KIRAZLI', 'latitude': '41.0322960516', 'longitude': '28.8427689525', 'id': 44, 'order': 1, 'line': 'M3'}
        ]

        # T1 corrections
        if len(self.stations['T1']) > 25:
            self.stations['T1'][25]["latitude"] = '41.015180'
            self.stations['T1'][25]["longitude"] = "28.975890"
            self.stations['T1'][25]["id"] = 330

        # T5 corrections
        if len(self.stations["T5"]) > 0:
            self.stations["T5"][0]["latitude"] = "41.0174770208"
            self.stations["T5"][0]["longitude"] = "28.9732097738"
            self.stations["T5"][0]["id"] = 78
        if len(self.stations["T5"]) > 12:
            self.stations["T5"][12]["latitude"] = "41.0791702"
            self.stations["T5"][12]["longitude"] = "28.9493602"
            self.stations["T5"][12]["id"] = 150

        # M1B complete data
        self.stations["M1B"] = [
            {'name': 'KIRAZLI', 'latitude': '41.0322960516', 'longitude': '28.8427689525', 'id': 44, 'order': 1, 'line': 'M1B'},
            {'name': 'BAGCILAR MEYDAN', 'latitude': '41.0345164689', 'longitude': '28.8561714937', 'id': 48, 'order': 2, 'line': 'M1B'},
            {'name': 'UCYUZLU', 'latitude': '41.036721597', 'longitude': '28.8706340581', 'id': 49, 'order': 3, 'line': 'M1B'},
            {'name': 'MENDERES', 'latitude': '41.0427591002', 'longitude': '28.8784878297', 'id': 50, 'order': 4, 'line': 'M1B'},
            {'name': 'ESENLER', 'latitude': '41.037682433', 'longitude': '28.8884222852', 'id': 51, 'order': 5, 'line': 'M1B'},
            {'name': 'OTOGAR', 'latitude': '41.0401441651', 'longitude': '28.8945600984', 'id': 211, 'order': 11, 'line': 'M1B'},
            {'name': 'KOCATEPE', 'latitude': '41.0484928183', 'longitude': '28.8953862076', 'id': 204, 'order': 12, 'line': 'M1B'},
            {'name': 'SAGMALCILAR', 'latitude': '41.0408544497', 'longitude': '28.9072352877', 'id': 205, 'order': 13, 'line': 'M1B'},
            {'name': 'BAYRAMPASA', 'latitude': '41.0340978572', 'longitude': '28.920238689', 'id': 206, 'order': 14, 'line': 'M1B'},
            {'name': 'ULUBATLI', 'latitude': '41.0240250582', 'longitude': '28.9305034257', 'id': 207, 'order': 15, 'line': 'M1B'},
            {'name': 'EMNIYET', 'latitude': '41.0176115439', 'longitude': '28.9395963977', 'id': 208, 'order': 16, 'line': 'M1B'},
            {'name': 'AKSARAY', 'latitude': '41.0120281897', 'longitude': '28.9480625565', 'id': 209, 'order': 17, 'line': 'M1B'},
            {'name': 'YENIKAPI', 'latitude': '41.0055971704', 'longitude': '28.9513306172', 'id': 20, 'order': 18, 'line': 'M1B'}
        ]

        # M1A complete data
        self.stations["M1A"] = [
            {'name': 'ATATURK HAVALIMANI', 'latitude': '40.9795429431', 'longitude': '28.8211244027', 'id': 105, 'order': 1, 'line': 'M1A'},
            {'name': 'DTM - ISTANBUL FUAR MERKEZI', 'latitude': '40.9866455145', 'longitude': '28.8285503243', 'id': 106, 'order': 2, 'line': 'M1A'},
            {'name': 'YENIBOSNA', 'latitude': '40.9893149835', 'longitude': '28.8367043004', 'id': 107, 'order': 3, 'line': 'M1A'},
            {'name': 'ATAKOY', 'latitude': '40.9913500997', 'longitude': '28.846082309', 'id': 108, 'order': 4, 'line': 'M1A'},
            {'name': 'BAHCELIEVLER', 'latitude': '40.9953532384', 'longitude': '28.8630661969', 'id': 109, 'order': 5, 'line': 'M1A'},
            {'name': 'BAKIRKOY - INCIRLI', 'latitude': '40.9966121333', 'longitude': '28.8753997556', 'id': 110, 'order': 6, 'line': 'M1A'},
            {'name': 'ZEYTINBURNU', 'latitude': '41.0014853458', 'longitude': '28.8902920022', 'id': 60, 'order': 7, 'line': 'M1A'},
            {'name': 'MERTER', 'latitude': '41.0076458753', 'longitude': '28.8961771147', 'id': 112, 'order': 8, 'line': 'M1A'},
            {'name': 'DAVUTPASA', 'latitude': '41.0206387059', 'longitude': '28.9001417888', 'id': 113, 'order': 9, 'line': 'M1A'},
            {'name': 'TERAZIDERE', 'latitude': '41.0303317032', 'longitude': '28.8979522419', 'id': 114, 'order': 10, 'line': 'M1A'},
            {'name': 'KOCATEPE', 'latitude': '41.0408544497', 'longitude': '28.9072352877', 'id': 205, 'order': 12, 'line': 'M1A'}
        ]

        # M6 corrections
        if len(self.stations["M6"]) > 0:
            self.stations["M6"][0]["latitude"] = "41.0767734293"
            self.stations["M6"][0]["longitude"] = "29.0136876237"
            self.stations["M6"][0]["id"] = 28

        # M9 corrections
        if len(self.stations["M9"]) > 2:
            self.stations["M9"][2]["latitude"] = "41.0724333906"
            self.stations["M9"][2]["longitude"] = "28.8023285305"
            self.stations["M9"][2]["id"] = 40

        # T4 corrections
        if len(self.stations["T4"]) > 7:
            self.stations["T4"][7]["latitude"] = "41.0815994"
            self.stations["T4"][7]["longitude"] = "28.8754204"
            self.stations["T4"][7]["id"] = 156
        if len(self.stations["T4"]) > 19:
            self.stations["T4"][19]["latitude"] = '41.0240250582'
            self.stations["T4"][19]["longitude"] = '28.9305034257'
            self.stations["T4"][19]["id"] = 207
        if len(self.stations["T4"]) > 21:
            self.stations["T4"][21]["latitude"] = '41.0192295429'
            self.stations["T4"][21]["longitude"] = '28.9194470285'
            self.stations["T4"][21]["id"] = 65

        # F1 corrections
        if len(self.stations["F1"]) > 0:
            self.stations["F1"][0]["latitude"] = '41.034195'
            self.stations["F1"][0]["longitude"] = '28.992712'
            self.stations["F1"][0]["id"] = 82
        if len(self.stations["F1"]) > 1:
            self.stations["F1"][1]["latitude"] = '41.038496'
            self.stations["F1"][1]["longitude"] = '28.985783'
            self.stations["F1"][1]["id"] = 24

        # F4 corrections
        if len(self.stations["F4"]) > 1:
            self.stations["F4"][1]["latitude"] = '41.085278'
            self.stations["F4"][1]["longitude"] = '29.045519'
            self.stations["F4"][1]["id"] = 141

    def build_graph(self):
        """Build NetworkX graph from station data"""
        # Add nodes
        for line_name, station_list in self.stations.items():
            for station in station_list:
                node_id = station['id']
                lat = float(station["latitude"])
                lng = float(station["longitude"])
                self.G.add_node(
                    node_id,
                    pos=(lng, lat),
                    name=station["name"],
                    line=line_name,
                    order=station["order"]
                )

        # Add edges (connections between consecutive stations on same line)
        for line_name, station_list in self.stations.items():
            for i in range(len(station_list) - 1):
                station1 = station_list[i]
                station2 = station_list[i + 1]

                # Calculate distance between stations
                distance = self._haversine_distance(
                    float(station1["latitude"]), float(station1["longitude"]),
                    float(station2["latitude"]), float(station2["longitude"])
                )

                # Add edge with distance as weight
                self.G.add_edge(
                    station1["id"],
                    station2["id"],
                    weight=distance,
                    line=line_name
                )

    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in kilometers"""
        R = 6371  # Earth's radius in kilometers

        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))

        return R * c

    def get_all_stations(self) -> Dict:
        """Get all stations grouped by line"""
        return self.stations

    def get_all_lines(self) -> Dict:
        """Get all metro lines with colors"""
        return self.line_colors

    def find_shortest_path(self, source_id: int, target_id: int) -> Optional[Dict]:
        """Find shortest path between two stations"""
        try:
            # Find path
            path = nx.shortest_path(self.G, source=source_id, target=target_id, weight='weight')

            # Calculate total distance and time
            total_distance = 0
            total_time = 0  # in minutes
            route_details = []

            for i in range(len(path) - 1):
                current_id = path[i]
                next_id = path[i + 1]

                # Get edge data
                edge_data = self.G.get_edge_data(current_id, next_id)
                distance = edge_data['weight']
                line = edge_data.get('line', 'Unknown')

                # Get station info
                current_station = self.G.nodes[current_id]
                next_station = self.G.nodes[next_id]

                # Calculate travel time (assuming average speed of 40 km/h + 1 min stop time)
                travel_time = (distance / 40) * 60 + 1  # minutes

                total_distance += distance
                total_time += travel_time

                route_details.append({
                    'from_id': current_id,
                    'from_name': current_station['name'],
                    'to_id': next_id,
                    'to_name': next_station['name'],
                    'line': line,
                    'distance': round(distance, 2),
                    'time': round(travel_time, 1)
                })

            # Build station list with details
            stations_on_route = []
            for station_id in path:
                station_data = self.G.nodes[station_id]
                stations_on_route.append({
                    'id': station_id,
                    'name': station_data['name'],
                    'latitude': station_data['pos'][1],
                    'longitude': station_data['pos'][0],
                    'line': station_data.get('line', 'Unknown')
                })

            return {
                'path': path,
                'stations': stations_on_route,
                'route_details': route_details,
                'total_distance': round(total_distance, 2),
                'total_time': round(total_time, 1),
                'num_stations': len(path)
            }
        except nx.NetworkXNoPath:
            return None
        except Exception as e:
            print(f"Error finding path: {e}")
            return None

    def get_station_by_id(self, station_id: int) -> Optional[Dict]:
        """Get station information by ID"""
        try:
            station_data = self.G.nodes[station_id]
            return {
                'id': station_id,
                'name': station_data['name'],
                'latitude': station_data['pos'][1],
                'longitude': station_data['pos'][0],
                'line': station_data.get('line', 'Unknown')
            }
        except KeyError:
            return None

    def search_stations(self, query: str) -> List[Dict]:
        """Search stations by name"""
        query = query.upper()
        results = []

        for node_id, data in self.G.nodes(data=True):
            if query in data['name'].upper():
                results.append({
                    'id': node_id,
                    'name': data['name'],
                    'latitude': data['pos'][1],
                    'longitude': data['pos'][0],
                    'line': data.get('line', 'Unknown')
                })

        return results
