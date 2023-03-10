from pathlib import Path
import pytest

import numpy as np
import pandas as pd

from sequitur.writer import write_parquet
from sequitur.reader import read_parquet


@pytest.fixture
def my_path(tmpdir):
    return Path(tmpdir, 'myfile.parquet')


@pytest.fixture
def minimum_example():
    return {
        'nid': np.array([0]),
        't': np.array([1]),
        'x': np.array([2])
    }


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


@pytest.fixture
def simple_nodes() -> dict[str, list]:
    """Return the nodes of a simple test graph."""
    return NODES


@pytest.fixture 
def simple_edges() -> dict[str, list]:
    """Return the edges of a simple test graph."""
    return EDGES


def test_write_dataframe(my_path, minimum_example):
    # create dataframe from dictionary
    dataframe = pd.DataFrame(minimum_example)

    # write file 
    write_parquet(my_path, dataframe)

    # check that it exists
    assert Path(my_path).exists()


def test_read_dataframe(my_path, minimum_example):
    # create dataframe from dictionary
    dataframe = pd.DataFrame(minimum_example)

    # write file 
    write_parquet(my_path, dataframe)

    # load
    read_dataframe = read_parquet(my_path)

    assert read_dataframe.to_pandas().equals(dataframe)
