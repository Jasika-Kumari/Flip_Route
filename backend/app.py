from flask import Flask, request, jsonify
from flask_cors import CORS
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

app = Flask(__name__)
CORS(app)

geolocator = Nominatim(user_agent="route-planner")

# Helper: Convert address to (lat, lon)
def geocode_address(address):
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

# Helper: Calculate straight-line distance
def haversine_distance(coord1, coord2):
    return geodesic(coord1, coord2).km

@app.route('/route', methods=['POST'])
def route():
    try:
        data = request.get_json(force=True)
        print("Received JSON:", data)
    except Exception as e:
        print(f"[ERROR] Invalid JSON: {e}")
        return jsonify({"error": "Invalid JSON format"}), 400

    start = data.get("start", "").strip()
    waypoints = data.get("waypoints", [])
    end = data.get("end", "").strip()
    optimize = data.get("optimize", "distance")

    if not start or not end:
        return jsonify({"error": "Start and end are required."}), 400

    # Geocode all addresses
    all_addresses = [start] + waypoints + [end]
    coords = []

    for address in all_addresses:
        try:
            coord = geocode_address(address)
            if not coord:
                raise ValueError(f"Could not geocode address: {address}")
            coords.append(coord)
        except Exception as e:
            print(f"[ERROR] Geocoding failed for '{address}': {e}")
            return jsonify({"error": f"Geocoding failed for '{address}'"}), 400

    # Optimize route using nearest-neighbor for 'distance' or 'time'
    ordered_coords = [coords[0]]
    remaining = coords[1:-1]
    current = coords[0]

    while remaining:
        next_point = min(remaining, key=lambda x: haversine_distance(current, x))
        ordered_coords.append(next_point)
        remaining.remove(next_point)
        current = next_point

    ordered_coords.append(coords[-1])  # End

    # Total distance
    total_distance = 0.0
    for i in range(len(ordered_coords) - 1):
        total_distance += haversine_distance(ordered_coords[i], ordered_coords[i + 1])

    # Estimate time (mock 40 km/h avg speed)
    avg_speed_kmph = 40
    travel_time_min = round((total_distance / avg_speed_kmph) * 60)

    return jsonify({
        "route_coords": ordered_coords,
        "distance_km": round(total_distance, 2),
        "travel_time_min": travel_time_min,
        "status": "success"
    })

if __name__ == '__main__':
    app.run(debug=True, port=8000)
