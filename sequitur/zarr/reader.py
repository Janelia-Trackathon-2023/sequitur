from pathlib import Path
from typing import Union

import numpy as np
import zarr

def read_zarr(path: Union[str, Path]) -> dict[np.ndarray]:
    if not Path(path).exists():
        raise ValueError(f'File {path} does not exists.')
    
    # open file
    zarr_array = zarr.open(path)

    # retrieve groups
    data = {}
    if 'raw' in zarr_array.keys():
        data['raw'] = zarr_array['raw'][:]
    if 'annotations' in zarr_array.keys():
        data['annotations'] = zarr_array['annotations'][:]

    return data
