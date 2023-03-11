# %%
"""
Load the example data and save it to our format.
"""
from pathlib import Path
import json
import pandas as pd
import zarr

from sequitur.format import EdgeEntries, NodeEntries
from sequitur.build_file import FileBuilder

# %%
# Load and shape data
path_to_file = Path('examples', 'sequitur')
builder = FileBuilder(path_to_file)

root = Path('examples', 'example_data')

# save images
data = zarr.open(Path(root, 'Fluo-N3DH-CHO.zarr'))
builder.add_images(data['images'][:], data['segmentations'][:])

with open(Path(root, 'candidate_graph.json'), 'r') as f:
  candidate_graph = json.load(f)

  # nodes
  nodes  = pd.DataFrame(candidate_graph['nodes'])
  nodes[NodeEntries.COORDINATES.value] = list(zip(nodes.t, nodes.x, nodes.y, nodes.z))
  nodes.drop(['t', 'x', 'y', 'z'], axis=1)

  # edges
  edges = pd.DataFrame(candidate_graph['links'])
  edges[EdgeEntries.ID.value] = [i for i in range(edges.shape[0])]

  # %%
  builder = FileBuilder(path_to_file)

  # create nodes and adges
  builder.add_graph(nodes, edges)
  

# %% 

