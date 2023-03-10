from pathlib import Path
from typing import Union

import zarr
import pyarrow.parquet as pq

def read_zarr(path: Union[str, Path]):
    if not Path(path).exists():
        raise ValueError(f'File {path} does not exists.')
    
    return zarr.open(path)

def read_parquet(path: Union[str, Path], **kwargs):
    return pq.read_table(path, **kwargs)