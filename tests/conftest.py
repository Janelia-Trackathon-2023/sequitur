import pytest


NODES = {
    "id": [0, 1, 2, 3, 4, 5, 6, 7],
    "x": [0, 1, 2, 2, 3, 3, 4, 5],
    "y": [1, 1, 2, 0, 2, 0, 1, 1],
    "z": [0, 0, 0, 0, 0, 0, 0, 0],
    "t": [0, 1, 2, 2, 3, 3, 4, 5],
}


EDGES = {
    "source": [0, 1, 1, 2, 3, 4, 5, 6],
    "target": [1, 2, 3, 4, 5, 6, 6, 7],
}


@pytest.fixture
def test_nodes() -> dict[str, list]:
    return NODES


@pytest.fixture 
def test_edges() -> dict[str, list]:
    return EDGES


