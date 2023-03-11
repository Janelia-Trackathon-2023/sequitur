import pytest


NODES = {
    "nid": [0, 1, 2, 3, 4, 5, 6, 7],
    "z": [0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 4.0, 5.0],
    "y": [1.0, 1.0, 2.0, 0.0, 2.0, 0.0, 1.0, 1.0],
    "x": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "t": [0, 1, 2, 2, 3, 3, 4, 5],
    "score": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
}


EDGES = {
    "eid": [0, 1, 2, 3, 4, 5, 6, 7],
    "source": [0, 1, 1, 2, 3, 4, 5, 6],
    "target": [1, 2, 3, 4, 5, 6, 6, 7],
    "score": [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    "score": [1, 0, 0, 1, 1, 0, 0, 1],
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
