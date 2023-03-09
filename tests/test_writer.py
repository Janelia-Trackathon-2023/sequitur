from pathlib import Path

import numpy as np
import pytest

from sequitur.format import Subgroup
from sequitur.writer import write


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
    pass
