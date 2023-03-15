from pathlib import Path
import pytest

import zarr
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
    sequ = SequiturFile(path, mode='w')
    assert not sequ.has_nodes
    assert not sequ.has_edges

    # create nodes
    path_to_nodes = Path(path, PATH_NODES)
    path_to_nodes.parent.mkdir(parents=True)

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
    path_to_edges.parent.mkdir(parents=True)

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
    