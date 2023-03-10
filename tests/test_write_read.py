from pathlib import Path

import numpy as np
import pytest

from sequitur.format import Subgroup, Group
from sequitur.writer import write_zarr
from sequitur.reader import read_zarr


@pytest.fixture
def my_path(tmpdir):
    return Path(tmpdir, 'myzarr.zarr')


@pytest.fixture
def minimum_example():
    return {
        Subgroup.NODES_ID.value: np.array([0]),
        Subgroup.NODES_T.value: np.array([1]),
        Subgroup.NODES_X.value: np.array([2]),

        Subgroup.EDGES_ID.value: np.array([3]),
        Subgroup.EDGES_SOURCE.value: np.array([4]),
        Subgroup.EDGES_TARGET.value: np.array([5]),
    }


NODES = {
    Subgroup.NODES_ID.value: [0, 1, 2, 3, 4, 5, 6, 7],
    Subgroup.NODES_X.value: [0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 4.0, 5.0],
    Subgroup.NODES_Y.value: [1.0, 1.0, 2.0, 0.0, 2.0, 0.0, 1.0, 1.0],
    Subgroup.NODES_Z.value: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    Subgroup.NODES_T.value: [0, 1, 2, 2, 3, 3, 4, 5],
    Subgroup.NODES_SCORE.value: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
}


EDGES = {
    Subgroup.EDGES_ID.value: [0, 1, 2, 3, 4, 5, 6, 7],
    Subgroup.EDGES_SOURCE.value: [0, 1, 1, 2, 3, 4, 5, 6],
    Subgroup.EDGES_TARGET.value: [1, 2, 3, 4, 5, 6, 6, 7],
    Subgroup.EDGES_SCORE.value: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    Subgroup.EDGES_SOLUTION.value: [1, 0, 0, 1, 1, 0, 0, 1],
}


TRACKS = {
    Subgroup.TRACKS_ID.value: [0, 1, 2, 3],
    Subgroup.TRACKS_BEGIN.value: [0, 2, 3, 6],
    Subgroup.TRACKS_END.value: [1, 4, 5, 7],
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
