from pathlib import Path
import pytest

import numpy as np
import pandas as pd

from sequitur.parquet.parquet_io import (
    _write_parquet_df, write_parquet, read_parquet, _write_parquet_api
)
from sequitur.format import NodeEntries
from sequitur.schema import NodeModel, EdgeModel

@pytest.fixture
def my_path(tmpdir):
    return Path(tmpdir, 'myfile.parquet')


@pytest.fixture
def minimum_example():
    return {
        NodeEntries.ID.value: np.array([0]),
        NodeEntries.COORDINATES.value: np.array([1])
    }


def test_write_dataframe(my_path, minimum_example):
    # create dataframe from dictionary
    dataframe = pd.DataFrame(minimum_example)

    # write file 
    _write_parquet_df(my_path, dataframe)

    # check that it exists
    assert Path(my_path).exists()


def test_read_dataframe(my_path, minimum_example):
    # create dataframe from dictionary
    dataframe = pd.DataFrame(minimum_example)

    # write file 
    _write_parquet_df(my_path, dataframe)

    # load
    read_dataframe = read_parquet(my_path)

    assert read_dataframe.to_pandas().equals(dataframe)


def test_read_write_nodes_edges(tmpdir, simple_nodes, simple_edges):
    write_parquet(tmpdir, simple_nodes, simple_edges)

    # check that files have been created
    assert Path(tmpdir, 'nodes.parquet').exists
    assert Path(tmpdir, 'edges.parquet').exists

    # compare nodes
    read_nodes = read_parquet(Path(tmpdir, 'nodes.parquet'))
    assert read_nodes.to_pandas().equals(pd.DataFrame(simple_nodes))

    # compare edges
    read_edges = read_parquet(Path(tmpdir, 'edges.parquet'))
    assert read_edges.to_pandas().equals(pd.DataFrame(simple_edges))

def test_io_api(tmpdir):
    nodes = [
        NodeModel(node_id=i, coordinates=(i,)) for i in range(5)
    ]

    path = Path(tmpdir, 'nodes.parquet')
    _write_parquet_api(path, nodes)

    assert path.exists()

    read_nodes = read_parquet(path)

    # read 
    fields = nodes[0].__fields__.keys()

    table = {}
    for f in fields:
        table.update(
            {
                f: [getattr(node, f) for node in nodes]
            }
        )
    assert read_nodes.to_pandas().equals(pd.DataFrame(table))
