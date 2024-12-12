import json
import networkx as nx

ENTRY = "https://cdn.star.nesdis.noaa.gov/GOES16/"

# Load the JSON data
with open("output.json", "r") as f:
    data = json.load(f)

# Create an empty network graph
G = nx.DiGraph()  # Use nx.Graph() for undirected graph


# "baseURL": "https://cdn.star.nesdis.noaa.gov/GOES16/",
# "relURL": "",
# "files": 0,
# "folders": 3,
# "extensions": {},

root = data[ENTRY]
print(root["baseURL"])
print(root["relURL"])
print(root["files"])
print(root["folders"])
print(root["extensions"])
print(len(root["children"]))