# Backend/utils/routing.py
import networkx as nx
import osmnx as ox
from geopy.distance import geodesic

def compute_route(G, coords, optimize="distance"):
    route_nodes = [ox.distance.nearest_nodes(G, lon, lat) for lat, lon in coords]

    full_route = []
    total_distance = 0.0

    for i in range(len(route_nodes) - 1):
        path = nx.shortest_path(G, route_nodes[i], route_nodes[i + 1], weight="length")
        full_route.extend(path[:-1])
    full_route.append(route_nodes[-1])

    route_coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in full_route]

    for i in range(len(route_coords) - 1):
        total_distance += geodesic(route_coords[i], route_coords[i + 1]).km

    travel_time_min = (total_distance / 40) * 60  # Assuming 40 km/h
    return route_coords, round(total_distance, 2), round(travel_time_min, 2)
