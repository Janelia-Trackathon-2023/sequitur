from pathlib import Path

from typing import Any, Union, List

import numpy as np
import zarr


def write_zarr(
        path: Union[str, Path], 
        data: np.ndarray, 
        annotations: np.ndarray= None
    ) -> None:

    if Path(path).exists():
        raise ValueError(f'File {path} already exists.')

    # create zarr groups
    root = zarr.open(path, mode='w')
    
    # raw and annotations image data
    root.array(name='raw', data=data)
    root.array(name='annotations', data=annotations)
    