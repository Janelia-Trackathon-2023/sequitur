from pathlib import Path
import pytest

import numpy as np

from sequitur.zarr.writer import write_zarr
from sequitur.zarr.reader import read_zarr
from sequitur.format import ZarrGroup


@pytest.fixture
def my_path(tmpdir):
    return Path(tmpdir, 'myfile.zarr')


@pytest.fixture
def minimum_img():
    return np.array([
        [0, 1, 2, 3],
        [0, 3, 5, 6],
        [0, 2, 0, 3],
    ], dtype=np.float16)


@pytest.fixture
def minimum_lbl():
    return np.array([
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 2],
    ], dtype=np.int16)


def test_write_arrays(my_path, minimum_img, minimum_lbl):
    write_zarr(my_path, minimum_img, minimum_lbl)

    assert my_path.exists()


def test_write_read_arrays(my_path, minimum_img, minimum_lbl):
    write_zarr(my_path, minimum_img, minimum_lbl)

    # read array
    read_data = read_zarr(my_path)

    # compare sub arrays
    assert (read_data[ZarrGroup.IMAGES.value][:] == minimum_img).all()
    assert (read_data[ZarrGroup.ANNOTATIONS.value][:] == minimum_lbl).all()
