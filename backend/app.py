# services/routing_service.py
import osmnx as ox
import networkx as nx
from itertools import permutations

GRAPH_PATH = "data/graphs/jharkhand/ranchi.graphml"
print("📦 Loading Ranchi GraphML...")
G = ox.load_graphml(GRAPH_PATH)
print("✅ Graph loaded.")

def get_optimized_route(start, end, waypoints, strategy="greedy"):
    # All coordinates: start + waypoints + end
    all_points = [start] + waypoints + [end]
    nodes = [ox.distance.nearest_nodes(G, p['lng'], p['lat']) for p in all_points]

    start_node = nodes[0]
    end_node = nodes[-1]
    wp_nodes = nodes[1:-1]

    # Optimize waypoint order
    if strategy == "brute" and len(wp_nodes) <= 6:
        path_nodes = find_best_route(G, start_node, wp_nodes, end_node)
    else:
        path_nodes = tsp_greedy(G, start_node, wp_nodes, end_node)

    # Create full route using shortest paths
    full_path = []
    total_distance = 0
    for i in range(len(path_nodes) - 1):
        segment = nx.shortest_path(G, path_nodes[i], path_nodes[i + 1], weight="length")
        full_path += segment if i == 0 else segment[1:]
        total_distance += nx.path_weight(G, segment, weight="length")

    route_coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in full_path]
    eta_min = total_distance / (35 * 1000 / 60)  # 35 km/hr average speed

    return {
        "route": route_coords,
        "distance_m": int(total_distance),
        "eta_min": round(eta_min, 2)
    }

def tsp_greedy(graph, start, waypoints, end):
    ordered = [start]
    current = start
    to_visit = waypoints.copy()

    while to_visit:
        next_node = min(to_visit, key=lambda x: nx.shortest_path_length(graph, current, x, weight="length"))
        ordered.append(next_node)
        to_visit.remove(next_node)
        current = next_node

    ordered.append(end)
    return ordered

def find_best_route(graph, start, waypoints, end):
    best_order = None
    best_distance = float("inf")

    for perm in permutations(waypoints):
        test_path = [start] + list(perm) + [end]
        dist = 0
        for i in range(len(test_path) - 1):
            dist += nx.shortest_path_length(graph, test_path[i], test_path[i + 1], weight="length")
        if dist < best_distance:
            best_distance = dist
            best_order = test_path

    return best_order
