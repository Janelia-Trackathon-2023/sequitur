import pytest

from sequitur.format import NodeEntries, EdgeEntries

NODES = {
    NodeEntries.ID.value: [0, 1, 2, 3, 4, 5, 6, 7],
    NodeEntries.COORDINATES.value: [0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 4.0, 5.0],
   # "y": [1.0, 1.0, 2.0, 0.0, 2.0, 0.0, 1.0, 1.0],
   # "x": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
   # "t": [0, 1, 2, 2, 3, 3, 4, 5],
    NodeEntries.SCORE.value: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
}


EDGES = {
    EdgeEntries.ID.value: [0, 1, 2, 3, 4, 5, 6, 7],
    EdgeEntries.SOURCE.value: [0, 1, 1, 2, 3, 4, 5, 6],
    EdgeEntries.TARGET.value: [1, 2, 3, 4, 5, 6, 6, 7],
    EdgeEntries.SCORE.value: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
}


# TRACKS = {
#     "tid": [0, 1, 2, 3],
#     "begin": [0, 2, 3, 6],
#     "end": [1, 4, 5, 7],
# }


@pytest.fixture
def simple_nodes() -> dict[str, list]:
    """Return the nodes of a simple test graph."""
    return NODES


@pytest.fixture 
def simple_edges() -> dict[str, list]:
    """Return the edges of a simple test graph."""
    return EDGES


# @pytest.fixture 
# def test_tracks() -> dict[str, list]:
#     """Return the tracks defined in the graph."""
#     return TRACKS
