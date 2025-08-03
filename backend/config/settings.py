import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GRAPH_DIR = os.path.join(BASE_DIR, "data", "graphs", "jharkhand")  # update this for every location also scale it for long term 

DEFAULT_CITY = "ranchi"
DEFAULT_GRAPH = os.path.join(GRAPH_DIR, f"{DEFAULT_CITY}.graphml")

SPEED_KMPH = 40
