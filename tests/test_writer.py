from pathlib import Path

import numpy as np
import pytest

from sequitur.format import Subgroup
from sequitur.writer import write


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


def test_writer(tmpdir, minimum_example):
    path = Path(tmpdir, 'myzarr.zarr')

    # write zarr to disk
    write(path, minimum_example)

    # simply assert existence
    assert path.exists()
