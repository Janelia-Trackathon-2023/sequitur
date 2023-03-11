from pathlib import Path
from typing import Union

import numpy as np
import zarr

from sequitur.format import ZarrGroup

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
    root.array(name=ZarrGroup.IMAGES.value, data=data)
    root.array(name=ZarrGroup.ANNOTATIONS.value, data=annotations)
    

def read_zarr(path: Union[str, Path]) -> dict[np.ndarray]:
    if not Path(path).exists():
        raise ValueError(f'File {path} does not exists.')
    
    # open file
    zarr_array = zarr.open(path)

    # retrieve groups
    data = {}
    if ZarrGroup.IMAGES.value in zarr_array.keys():
        data[ZarrGroup.IMAGES.value] = zarr_array[ZarrGroup.IMAGES.value][:]
    if ZarrGroup.ANNOTATIONS.value in zarr_array.keys():
        data[ZarrGroup.ANNOTATIONS.value] = zarr_array[ZarrGroup.ANNOTATIONS.value][:]

    return data
