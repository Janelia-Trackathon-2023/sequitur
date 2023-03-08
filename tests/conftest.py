import pytest


NODES = {
    "id": [0, 1, 2, 3, 4, 5, 6, 7],
    "x": [0, 1, 2, 2, 3, 3, 4, 5],
    "y": [1, 1, 2, 0, 2, 0, 1, 1],
    "z": [0, 0, 0, 0, 0, 0, 0, 0],
    "t": [0, 1, 2, 2, 3, 3, 4, 5],
}


EDGES = {
    "id": [0, 1, 2, 3, 4, 5, 6, 7],
    "source": [0, 1, 1, 2, 3, 4, 5, 6],
    "target": [1, 2, 3, 4, 5, 6, 6, 7],
}

TRACKS = {
    "id": [0, 1, 2, 3],
    "begin": [0, 2, 3, 6],
    "end": [1, 4, 5, 7,]
}


@pytest.fixture
def test_nodes() -> dict[str, list]:
    """Return the nodes of a simple test graph."""
    return NODES


@pytest.fixture 
def test_edges() -> dict[str, list]:
    """Return the edges of a simple test graph."""
    return EDGES


@pytest.fixture 
def test_tracks() -> dict[str, list]:
    """Return the tracks defined in the graph."""
    return TRACKS


