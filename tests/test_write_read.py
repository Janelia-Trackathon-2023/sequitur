from pathlib import Path

import numpy as np
import pytest

from sequitur.format import Subgroup, Group
from sequitur.writer import write
from sequitur.reader import read


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


def test_writer(my_path, minimum_example):
    # write zarr to disk
    write(my_path, minimum_example)

    # simply assert existence
    assert my_path.exists()


def test_write_read(my_path, minimum_example):
    # write zarr to disk
    write(my_path, minimum_example)

    # read it again
    mydata = read(my_path)

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

