from pathlib import Path

from typing import Union

import pandas as pd
import numpy as np

from sequitur.format import NodeEntries, EdgeEntries, FileNames
from sequitur.parquet.parquet_io import write_parquet
from sequitur.zarr.zarr_io import write_zarr


class SequiturFile:
    pass



# TODO: read/write flag
def open(path: Union[str, Path]):
    pass