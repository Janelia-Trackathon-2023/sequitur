from pathlib import Path
from typing import Union

import pyarrow.parquet as pq

def read_parquet(path: Union[str, Path], **kwargs):
    return pq.read_table(path, **kwargs)