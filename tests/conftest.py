import pytest

from sequitur.format import NodeEntries, EdgeEntries, TrackEntries


NODES = {
    NodeEntries.ID: [0, 1, 2, 3, 4, 5, 6, 7],
    NodeEntries.COORDINATES: [
        (0.0, 1.0, 0.0, 0), 
        (1.0, 1.0, 0.0, 1), 
        (2.0, 2.0, 0.0, 2), 
        (2.0, 0.0, 0.0, 2), 
        (3.0, 2.0, 0.0, 3), 
        (3.0, 0.0, 0.0, 3), 
        (4.0, 1.0, 0.0, 4), 
        (5.0, 1.0, 0.0, 5)
    ],
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
def simple_nodes() -> dict[str, list]:
    """Return the nodes of a simple test graph."""
    return NODES


@pytest.fixture 
def simple_edges() -> dict[str, list]:
    """Return the edges of a simple test graph."""
    return EDGES


@pytest.fixture 
def simple_tracks() -> dict[str, list]:
    """Return the tracks defined in the graph."""
    return TRACKS
