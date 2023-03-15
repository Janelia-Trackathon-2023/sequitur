from pathlib import Path
import pytest

import zarr
from pandas import DataFrame

from sequitur.parquet.parquet_io import write_parquet_df
from sequitur.sequitur import SequiturFile
from sequitur.format import *

def test_instantiate_non_existing(tmpdir):
    path = Path(tmpdir, 'myfolder')

    with pytest.raises(ValueError):
        SequiturFile(path, mode='r')

def test_instantiate_existing(tmpdir):
    path = Path(tmpdir, 'myfolder')

    SequiturFile(path, mode='w')
    assert path.exists()

def test_existing_zarr(tmpdir):
    path = Path(tmpdir, 'myfolder')
    path.mkdir()

    # check that a Sequitur file sees no images and labels
    sequ = SequiturFile(path, mode='r')
    assert not sequ.has_images
    assert not sequ.has_annotations

    # create zarr with only raw image data
    path_to_zarr = Path(path, PATH_IMAGE)
    my_zarr = zarr.open(path_to_zarr)
    image = my_zarr.zeros(ZarrGroup.IMAGES, shape=(16, 16), dtype='f4')

    # check that a Sequitur file can read it 
    sequ = SequiturFile(path, mode='r')
    assert sequ.has_images
    assert not sequ.has_annotations

    # get image array
    read_image = sequ.read_image()
    assert read_image == image

    # add annotations
    labels = my_zarr.zeros(ZarrGroup.ANNOTATIONS, shape=(16, 16), dtype='i4')

    # create new file
    sequ = SequiturFile(path, mode='r')
    assert sequ.has_images
    assert sequ.has_annotations

    # get labels array
    read_labels = sequ.read_annotations()
    assert read_labels == labels


def test_existing_nodes_and_edges(tmpdir, example_nodes, example_edges):
    path = Path(tmpdir, 'myfolder')
    path.mkdir()

    # check that a Sequitur file sees no nodes
    sequ = SequiturFile(path, mode='r')
    assert not sequ.has_nodes
    assert not sequ.has_edges

    # create nodes
    path_to_nodes = Path(path, PATH_NODES)
    path_to_nodes.parent.mkdir(parents=True)
    nodes = DataFrame(example_nodes)
    write_parquet_df(path_to_nodes, nodes)
    assert path_to_nodes.exists()

    # check that a Sequitur file sees nodes
    sequ = SequiturFile(path, mode='r')
    assert sequ.has_nodes
    assert not sequ.has_edges

    # read nodes
    read_nodes = sequ.read_nodes()
    assert read_nodes.equals(nodes)

    # create edges
    path_to_edges = Path(path, PATH_EDGES)
    path_to_edges.parent.mkdir(parents=True)
    edges = DataFrame(example_edges)
    write_parquet_df(path_to_edges, edges)
    assert path_to_edges.exists()

    # check that a Sequitur file sees edges
    sequ = SequiturFile(path, mode='r')
    assert sequ.has_nodes
    assert sequ.has_edges

    # read nodes
    read_edges = sequ.read_edges()
    assert read_edges.equals(edges)