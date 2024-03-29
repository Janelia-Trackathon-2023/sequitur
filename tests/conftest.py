import pytest

import pandas as pd

from sequitur.format import NodeEntries, EdgeEntries, TrackEntries
from sequitur.schema import NodeModel, EdgeModel

# NODES = {
#     NodeEntries.ID: [0, 1, 2, 3, 4, 5, 6, 7],
#     NodeEntries.COORDINATES: [
#         (0.0, 1.0, 0.0, 0), 
#         (1.0, 1.0, 0.0, 1), 
#         (2.0, 2.0, 0.0, 2), 
#         (2.0, 0.0, 0.0, 2), 
#         (3.0, 2.0, 0.0, 3), 
#         (3.0, 0.0, 0.0, 3), 
#         (4.0, 1.0, 0.0, 4), 
#         (5.0, 1.0, 0.0, 5)
#     ],
#     NodeEntries.SCORE: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
# }

NODES = {
    NodeEntries.ID: [0, 1, 2, 3, 4, 5, 6, 7],
    "z": [0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 4.0, 5.0],
    "y": [1.0, 1.0, 2.0, 0.0, 2.0, 0.0, 1.0, 1.0],
    "x": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "t": [0, 1, 2, 2, 3, 3, 4, 5],
    NodeEntries.SCORE: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
}

EDGES = {
    EdgeEntries.ID: [0, 1, 2, 3, 4, 5, 6, 7],
    EdgeEntries.SOURCE: [0, 1, 1, 2, 3, 4, 5, 6],
    EdgeEntries.TARGET: [1, 2, 3, 4, 5, 6, 6, 7],
    EdgeEntries.SCORE: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
}


TRACKS = {
    TrackEntries.ID: [0, 1, 2, 3],
    TrackEntries.START: [0, 2, 3, 6],
    TrackEntries.END: [1, 4, 5, 7],
}


@pytest.fixture
def example_nodes() -> dict[str, list]:
    """Return the nodes of a simple test graph."""
    return NODES


@pytest.fixture
def example_edges() -> dict[str, list]:
    """Return the edges of a simple test graph."""
    return EDGES


@pytest.fixture
def example_nodes_as_lst() -> list[NodeModel]:
    """Return the nodes of a simple test graph."""
    rows_as_dict = pd.DataFrame(NODES).to_dict(orient='records')

    return [
        NodeModel(**row) for row in rows_as_dict
    ]


@pytest.fixture 
def example_edges_as_lst() -> list[EdgeModel]:
    """Return the edges of a simple test graph."""
    rows_as_dict = pd.DataFrame(EDGES).to_dict(orient='records')

    return [
        EdgeModel(**row) for row in rows_as_dict
    ]



@pytest.fixture 
def example_tracks() -> dict[str, list]:
    """Return the tracks defined in the graph."""
    return TRACKS
