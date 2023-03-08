from pathlib import Path

import numpy as np
import pytest

from sequitur.format import Subgroup
from sequitur.writer import write

def test_writer(tmpdir):
    path = Path(tmpdir, 'myzarr')
    data = {
        Subgroup.NODES_ID.value: np.array([0]),
        Subgroup.NODES_T: np.array([1]),
        Subgroup.NODES_X: np.array([2]),

        Subgroup.EDGES_ID.value: np.array([3]),
        Subgroup.EDGES_SOURCE: np.array([4]),
        Subgroup.EDGES_TARGET: np.array([5]),
    }

    write(path, data)
