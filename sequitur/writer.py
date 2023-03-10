from pathlib import Path
from typing import Union, List

import zarr
from pandas import DataFrame
import pyarrow as pa
import pyarrow.parquet as pq

# TODO take image as input
def write_zarr(path: Union[str, Path], data: dict) -> None:
    # TODO: do we want to be able to override?
    # TODO check for .zarr? add .zarr?
    if Path(path).exists():
        raise ValueError(f'File {path} already exists.')

    # create zarr groups
    root = zarr.open(path, mode='w')

    # TODO write image


def write(path: Union[str, Path], list_dataframes: List[DataFrame]):
    pass


def write_parquet(path: Union[str, Path], dataframe: DataFrame):
    table = pa.Table.from_pandas(dataframe)
    pq.write_table(table, path)
