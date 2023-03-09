# %%
# Preparation: 
# - Create an environment, install motile and napari
# conda create -n trackathon -c conda-forge -c funkelab -c gurobi ilpy napari
# conda activate trackathon
# pip install motile
# - Clone and install the ctctools (as editable)
# git clone ...
# cd ctc-tools
# git switch trackathon
# pip install -e .
# - Create a folder called "data" in working directory
from ctctools import load_ctc, load_images
import napari
import urllib.request
import zipfile
from tqdm import tqdm
from scipy.spatial.distance import cdist
import itertools
from pathlib import Path
import networkx as nx
import motile
from motile.costs import NodeSelection, EdgeSelection, Appear
from motile.constraints import MaxParents, MaxChildren
from motile.variables import NodeSelected, EdgeSelected

# %%
# Add a utility to make a progress bar when downloading the file
url = "http://data.celltrackingchallenge.net/training-datasets/Fluo-N2DH-GOWT1.zip"
base_dir = Path("data")
filename = url.split('/')[-1]
ds_name = filename.split('.')[0]
class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

# %%
if not (base_dir / filename).exists():
    print(f"Downloading {ds_name} data from the CTC website")
    # Downloading data
    with DownloadProgressBar(unit='B', unit_scale=True,
                                miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, base_dir / filename, reporthook=t.update_to)
    # Unzip the data
    # TODO add a progress bar to zip as well
    with zipfile.ZipFile(base_dir / filename, 'r') as zip_ref:
        zip_ref.extractall(base_dir)

# %%
# Get detections
detections, graph = load_ctc(str(base_dir / ds_name), experiment="01")
# Load the raw and segmentations
images = load_images(str(base_dir / ds_name), experiment="01")
segmentations = load_images(str(base_dir / ds_name), experiment="01_ST/SEG")
# %%
viewer = napari.Viewer()
viewer.add_image(images, name="Raw")
viewer.add_labels(segmentations, name="Segmentations")
viewer.add_tracks(detections.to_numpy(), graph=graph, name="Tracks")

# %%
# PART 2 : Tracking with motile
# Adding a Positive score to the nodes to encourage selecting them.
scored_detections = detections.copy()
scored_detections["score"] = 1
cells = scored_detections.reset_index().rename(columns={"index": "id"})[["id", "t", "x", "y", "score"]].to_dict("records") 
    
# %%
edges = [
    # edge for every pair in t and t+1
    # with score the euclidian distance between edges
]
start_t = detections["t"].min()
end_t = detections["t"].max()

for t in range(start_t, end_t):
    prev_cells = detections[detections["t"] == t]
    next_cells = detections[detections["t"] == t + 1]
    # This gives pairwise distances as an array where the first index is time t and the second is time t + 1
    distances = cdist(prev_cells[["x", "y"]], next_cells[["x", "y"]])

    prev = range(len(prev_cells))
    next = range(len(next_cells))
    for i, j in itertools.product(prev, next):
        edges.append({"source": prev_cells.index[i], "target": next_cells.index[j], "distance": distances[i, j]})

# %%
# Create a motile candidate graph from detections
track_graph = motile.TrackGraph()
track_graph.add_nodes_from([
    (cell['id'], cell)
    for cell in cells
])
track_graph.add_edges_from([
    (edge['source'], edge['target'], edge)
    for edge in edges
])
# %%
solver = motile.Solver(track_graph)
# Add costs for nodes and edges
# Constant node selection cost, to ensure we choose cells
solver.add_costs(
    NodeSelection(
        weight=-100,
        attribute="score",
    )
)
# Edge cost proportional to the distance between detections
solver.add_costs(
    EdgeSelection(
        weight=1.0,
        attribute='distance'))

# Add a cost for appearance
# In general, we prefer divisions over appearances!
solver.add_costs(Appear(constant=10000.0))

# Add constraints for divisions
solver.add_constraints(MaxParents(1))
solver.add_constraints(MaxChildren(2))

# %%
# Solve
solution = solver.solve()

# %%
# PART 3: Adding solution as napari tracks
# Graph for napari is a dictionary with:
# key = a node
# value = a list of parents (in our case, parent*)
node_selected = solver.get_variables(NodeSelected)
edge_selected = solver.get_variables(EdgeSelected)

selected_nodes = []
selected_edges = []
for node in track_graph.nodes:
  if solution[node_selected[node]] > 0.5:
    selected_nodes.append(node)
for u, v in track_graph.edges:
  if solution[edge_selected[(u, v)]] > 0.5:
      selected_edges.append((u, v))
# %%
print(f"Selected {100*(len(selected_nodes) / len(cells))}% of all candidate nodes")
print(f"Selected {100*(len(selected_edges) / len(edges))}% of all candidate edges")
# %%
# Convert the solution to a napari track graph
# First we create a solution graph with only the selected parts
solution_graph = motile.TrackGraph()
for id in selected_nodes: 
    solution_graph.add_node(id, attrs=cells[id])
for u,v in selected_edges:
    solution_graph.add_edge(u, v)

# %%
# Next we get division points! 
# Since the id of the tracks is going to be specified later, we just keep the resulting edges in a list
divisions = [id for id, degree in solution_graph.out_degree() if degree > 1]
division_edges = [
    (div, k)
    for div in divisions
    for k in solution_graph[div]
]
# %%
# Remove division edges from solution graph
solution_graph.remove_edges_from(division_edges)
# This allows us to get all tracks as connected components
components = [c for c in nx.weakly_connected_components(solution_graph)]
# %% 
# We assign a "track_id" to each of the connected components.
import numpy as np
solution_detections = detections[["GT_ID", "t", "x", "y"]].copy()
solution_detections["track_id"] = np.nan
for i, c in enumerate(components):
    solution_detections["track_id"][list(components[i])] = i

# %%
# Now that we have track ids, we can create a division graph for napari's track layer
division_graph = {}
for parent, child in division_edges:
    parent_id = solution_detections.loc[parent]["track_id"]
    child_id = solution_detections.loc[child]["track_id"]
    division_graph[int(child_id)] = [int(parent_id)]
# %%
# Finally, we re-order the solutions the way that napari expects them, and view.
to_view = solution_detections[["cell_id", "t", "x", "y"]]
viewer.add_tracks(to_view.to_numpy(), graph=division_graph, name="Solution")

