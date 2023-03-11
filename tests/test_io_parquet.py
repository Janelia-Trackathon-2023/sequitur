from pathlib import Path
import pytest

import numpy as np
import pandas as pd

from sequitur.parquet.writer import _write_parquet, write
from sequitur.parquet.reader import read_parquet


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


def test_write_dataframe(my_path, minimum_example):
    # create dataframe from dictionary
    dataframe = pd.DataFrame(minimum_example)

    # write file 
    _write_parquet(my_path, dataframe)

    # check that it exists
    assert Path(my_path).exists()


def test_read_dataframe(my_path, minimum_example):
    # create dataframe from dictionary
    dataframe = pd.DataFrame(minimum_example)

    # write file 
    _write_parquet(my_path, dataframe)

    # load
    read_dataframe = read_parquet(my_path)

    assert read_dataframe.to_pandas().equals(dataframe)


def test_read_write_nodes_edges(tmpdir, simple_nodes, simple_edges):
    write(tmpdir, simple_nodes, simple_edges)

    # check that files have been created
    assert Path(tmpdir, 'nodes.parquet').exists
    assert Path(tmpdir, 'edges.parquet').exists

    # compare nodes
    read_nodes = read_parquet(Path(tmpdir, 'nodes.parquet'))
    assert read_nodes.to_pandas().equals(pd.DataFrame(simple_nodes))

    # compare edges
    read_edges = read_parquet(Path(tmpdir, 'edges.parquet'))
    assert read_edges.to_pandas().equals(pd.DataFrame(simple_edges))
