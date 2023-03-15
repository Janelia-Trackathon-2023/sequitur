from pathlib import Path
import pytest

import zarr

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
    path_to_zarr = Path(path, PATH_IMAGE)

    # create zarr with only raw image data
    my_zarr = zarr.open(path_to_zarr)
    image = my_zarr.create_group(ZarrGroup.IMAGES)
    image.zeros('raw', shape=(16, 16), dtype='f4')

    # check that a Sequitur file can read it 
    sequ = SequiturFile(path, mode='r')
    assert sequ.has_images
    assert not sequ.has_annotations

    # add annotations
    labels = my_zarr.create_group(ZarrGroup.ANNOTATIONS)
    labels.zeros('label', shape=(16, 16), dtype='i4')

    # create new file
    sequ = SequiturFile(path, mode='r')
    assert sequ.has_images
    assert sequ.has_annotations


