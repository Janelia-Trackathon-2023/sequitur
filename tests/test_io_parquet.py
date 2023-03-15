from pathlib import Path
import pytest

import numpy as np
import pandas as pd

from sequitur.parquet.parquet_io import (
    _read_parquet_df,
    read_nodes,
    read_edges,
    read_graph,
    read_nodes_as_df,
    read_edges_as_df,
    _write_parquet_from_list, 
    write_parquet_df,
    write_nodes,
)
from sequitur.format import NodeEntries

@pytest.fixture
def my_path(tmpdir):
    return Path(tmpdir, 'myfile.parquet')


def test_write_dataframe(my_path, example_edges):
    # create dataframe from dictionary
    dataframe = pd.DataFrame(example_edges)

    # write file 
    write_parquet_df(my_path, dataframe)

    # check that it exists
    assert Path(my_path).exists()


def test_read_dataframe(my_path, example_edges):
    """
    
    """
    # create dataframe from dictionary
    dataframe = pd.DataFrame(example_edges)

    # write file 
    write_parquet_df(my_path, dataframe)

    # load
    read_dataframe = _read_parquet_df(my_path)
    
    # # try coercing the lists to tuples
    # coerced_df = read_dataframe.astype({"coordinates": tuple})
    # coerced_df = coerced_df.convert_dtypes()

    assert read_dataframe.equals(dataframe)


# def test_io_nodemodel(tmpdir, example_nodes_as_lst, axis_order):
#     # write nodes
#     path = Path(tmpdir)
#     # _write_parquet_from_list(path, example_nodes_as_lst)\
#     write_nodes(path, example_nodes_as_lst, axis_order=axis_order)

#     assert path.exists()

#     # read the file back
#     nodes_read = read_nodes(path)

#     assert nodes_read == example_nodes_as_lst


# def test_io_edgemodel(tmpdir, example_edges_as_lst):
#     # write edges
#     path = Path(tmpdir, 'edges.parquet')
#     _write_parquet_from_list(path, example_edges_as_lst)

#     assert path.exists()

#     # read the file back
#     edges_read = read_edges(path)

#     assert edges_read == example_edges_as_lst


# def test_io_graph(tmpdir, example_nodes_as_lst, example_edges_as_lst):
#     # write nodes
#     node_path = Path(tmpdir, 'nodes.parquet')
#     _write_parquet_from_list(node_path, example_nodes_as_lst)

#     # write edges
#     edge_path = Path(tmpdir, 'edges.parquet')
#     _write_parquet_from_list(edge_path, example_edges_as_lst)

#     # read the file back
#     graph = read_graph(node_path, edge_path)

#     assert graph.nodes == example_nodes_as_lst
#     assert graph.edges == example_edges_as_lst


