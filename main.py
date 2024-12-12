import json
import numpy as np
import networkx as nx
import plotly.graph_objects as go

ENTRY = "https://cdn.star.nesdis.noaa.gov/GOES16/"
DATA_FILE = "dataset.json"

# Load the JSON data
with open("dataset.json", "r") as f:
    data = json.load(f)

# Initialize NetworkX graph
G = nx.DiGraph()

# Helper function to recursively parse the JSON and add nodes and edges
def parse_data(node, parent_url=None):
    base_url = str(node["baseURL"] + node["relURL"]).lstrip(ENTRY)
    G.add_node(base_url, files=node["files"], folders=node["folders"], extensions=node["extensions"])
    if parent_url:
        G.add_edge(parent_url, base_url)
    for child in node["children"]:
        for child_url, child_data in child.items():
            parse_data(child_data, base_url)

# Start parsing from the root node
root = data[ENTRY]
parse_data(root)

# Extract node positions using a layout algorithm
pos = nx.spring_layout(G, seed=420)

# Extract node attributes for visualization
node_x = [pos[node][0] for node in G.nodes]
node_y = [pos[node][1] for node in G.nodes]
node_files = [G.nodes[node]['files'] for node in G.nodes]
node_hover_texts = [
    f"URL: {node}<br>Files: {G.nodes[node]['files']}<br>Folders: {G.nodes[node]['folders']}<br>Extensions: {G.nodes[node]['extensions']}"
    for node in G.nodes
]

# Normalize files count to a logarithmic scale for coloring
min_files = 0
max_files = max(node_files)
node_colors = [np.log1p(files - min_files + 1) / np.log1p(max_files - min_files + 1) for files in node_files]
one_third_files = np.expm1((2 * np.log1p(min_files - min_files + 1) + np.log1p(max_files - min_files + 1)) / 3) + min_files - 1
two_thirds_files = np.expm1((np.log1p(min_files - min_files + 1) + 2 * np.log1p(max_files - min_files + 1)) / 3) + min_files - 1


# Create edge traces
edge_x = []
edge_y = []

for edge in G.edges:
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])  # None separates edges in the plot
    edge_y.extend([y0, y1, None])

edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=0.5, color="#888"),
    hoverinfo="none",
    mode="lines",
)

# Create node traces
node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers+text",
    marker=dict(
        size=10,
        color=node_colors,
        colorscale="Viridis", # my favorite color scheme!
        colorbar=dict(
            title="Files (Log)",
            tickvals=[0, 1 / 3, 2 / 3, 1],
            ticktext=[
                f"Min: {min_files}",
                f"1/3: {int(one_third_files)}",
                f"2/3: {int(two_thirds_files)}",
                f"Max: {max_files}",
            ],
            len=0.8,  
            yanchor="middle",  # Align color bar vertically
            y=0.5
        ),
        line=dict(width=2, color="black"),
    ),
    hoverinfo="text",
    hovertext=node_hover_texts,
)

# Create the figure
fig = go.Figure(data=[edge_trace, node_trace])

# Update layout
fig.update_layout(
    showlegend=False,
    hovermode="closest",
    margin=dict(b=0, l=0, r=0, t=0),
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False),
    title="NOAA Satellite Files Visualization",
)

# Show the plot
fig.show()
