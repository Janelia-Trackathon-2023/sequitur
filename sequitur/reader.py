from pathlib import Path
from typing import Union

import zarr

def read(path: Union[str, Path]):
    if not Path(path).exists():
        raise ValueError(f'File {path} does not exists.')
    
    return zarr.open(path)
