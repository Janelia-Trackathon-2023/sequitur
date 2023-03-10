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


def test_writer(my_path, minimum_example):
    # write zarr to disk
    write_zarr(my_path, minimum_example)

    # simply assert existence
    assert my_path.exists()


def test_read_mandatory(my_path, minimum_example):
    # write zarr to disk
    write_zarr(my_path, minimum_example)

    # read it again
    mydata = read_zarr(my_path)

    # compare data
    nodes_id = f'{Group.NODES.value}/{Subgroup.NODES_ID.value}'
    nodes_t = f'{Group.NODES.value}/{Subgroup.NODES_T.value}'
    nodes_x = f'{Group.NODES.value}/{Subgroup.NODES_X.value}'
    edges_id = f'{Group.EDGES.value}/{Subgroup.EDGES_ID.value}'
    edges_source = f'{Group.EDGES.value}/{Subgroup.EDGES_SOURCE.value}'
    edges_target = f'{Group.EDGES.value}/{Subgroup.EDGES_TARGET.value}'

    assert mydata[nodes_id][0] == minimum_example[Subgroup.NODES_ID.value][0]
    assert mydata[nodes_t][0] == minimum_example[Subgroup.NODES_T.value][0]
    assert mydata[nodes_x][0] == minimum_example[Subgroup.NODES_X.value][0]
    assert mydata[edges_id][0] == minimum_example[Subgroup.EDGES_ID.value][0]
    assert mydata[edges_source][0] == minimum_example[Subgroup.EDGES_SOURCE.value][0]
    assert mydata[edges_target][0] == minimum_example[Subgroup.EDGES_TARGET.value][0]


def test_read_simple_example(my_path, simple_nodes, simple_edges, simple_tracks):
    data_ref = {}
    data_ref.update(simple_nodes)
    data_ref.update(simple_edges)
    data_ref.update(simple_tracks)

    # write zarr to disk
    write_zarr(my_path, data_ref)

    # read it again
    data_read = read_zarr(my_path)

    # zarr keys
    nodes_id = f'{Group.NODES.value}/{Subgroup.NODES_ID.value}'
    nodes_t = f'{Group.NODES.value}/{Subgroup.NODES_T.value}'
    nodes_z = f'{Group.NODES.value}/{Subgroup.NODES_Z.value}'
    nodes_x = f'{Group.NODES.value}/{Subgroup.NODES_X.value}'
    nodes_y = f'{Group.NODES.value}/{Subgroup.NODES_Y.value}'
    nodes_score = f'{Group.NODES.value}/{Subgroup.NODES_SCORE.value}'

    edges_id = f'{Group.EDGES.value}/{Subgroup.EDGES_ID.value}'
    edges_source = f'{Group.EDGES.value}/{Subgroup.EDGES_SOURCE.value}'
    edges_target = f'{Group.EDGES.value}/{Subgroup.EDGES_TARGET.value}'
    edges_score = f'{Group.EDGES.value}/{Subgroup.EDGES_SCORE.value}'
    edges_solution = f'{Group.EDGES.value}/{Subgroup.EDGES_SOLUTION.value}'
    
    tracks_id = f'{Group.TRACKS.value}/{Subgroup.TRACKS_ID.value}'
    tracks_begin = f'{Group.TRACKS.value}/{Subgroup.TRACKS_BEGIN.value}'
    tracks_end = f'{Group.TRACKS.value}/{Subgroup.TRACKS_END.value}'

    
    # compare dictionaries
    assert (data_read[nodes_id][:] == NODES[Subgroup.NODES_ID.value]).all()
    assert (data_read[nodes_t][:] == NODES[Subgroup.NODES_T.value]).all()
    
    
    # TODO continue
    pass
