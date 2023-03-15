from pathlib import Path
import pytest

import zarr
import numpy as np
from pandas import DataFrame

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
    sequ = SequiturFile(path, mode='w')
    assert not sequ.has_images
    assert not sequ.has_annotations

    # create zarr with only raw image data
    image = np.array([
        [1, 3, 5.],
        [6, 2.3, 9]
    ])
    sequ.write_image(image)

    path_to_zarr = Path(path, PATH_IMAGE)
    assert path_to_zarr.exists()

    assert sequ.has_images
    assert not sequ.has_annotations

    # get image array
    read_image = sequ.read_image()
    assert (read_image == image).all()

    # add annotations
    labels = np.array([
        [0, 1, 2],
        [3, 4, 5]
    ])

    # create new file
    #sequ = SequiturFile(path, mode='r')
    #assert sequ.has_images
    #assert sequ.has_annotations

    # get labels array
    #read_labels = sequ.read_annotations()
    #assert read_labels == labels


def test_existing_nodes_and_edges(tmpdir, example_nodes, example_edges):
    path = Path(tmpdir, 'myfolder')
    path.mkdir()

    # check that a Sequitur file sees no nodes
    sequ = SequiturFile(path, mode='w')
    assert not sequ.has_nodes
    assert not sequ.has_edges

    # create nodes
    path_to_nodes = Path(path, PATH_NODES)
    nodes = DataFrame(example_nodes)
    sequ.write_nodes(nodes)
    
    assert path_to_nodes.exists()
    assert sequ.has_nodes
    assert not sequ.has_edges

    # read nodes
    read_nodes = sequ.read_nodes()
    assert read_nodes.equals(nodes)

    # create edges
    path_to_edges = Path(path, PATH_EDGES)
    edges = DataFrame(example_edges)
    sequ.write_edges(edges)

    assert path_to_edges.exists()
    assert sequ.has_nodes
    assert sequ.has_edges

    # read nodes
    read_edges = sequ.read_edges()
    assert read_edges.equals(edges)

    # and that a second file can as well
    sequ2 = SequiturFile(path, 'r')
    assert sequ2.read_nodes().equals(read_nodes)
    assert sequ2.read_edges().equals(read_edges)
