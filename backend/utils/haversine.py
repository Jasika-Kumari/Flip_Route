# Backend/utils/haversine.py
from geopy.distance import geodesic

def haversine_distance(coord1, coord2):
    return geodesic(coord1, coord2).km