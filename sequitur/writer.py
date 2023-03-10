from pathlib import Path
from typing import Union, Tuple
import warnings

import zarr
from pandas import DataFrame
import pyarrow as pa
import pyarrow.parquet as pq

from .format import Group, Subgroup

def write_zarr(path: Union[str, Path], data: dict) -> None:

    # TODO validate or impose in method signature the minimum dict keys
    missing_keys, unknown_keys = _validate(data)

    # TODO move the validation errors and warnings to _validate?
    # if there are missing keys, raise error
    if missing_keys:
        raise ValueError(f'The following mandatory keys are missing: {missing_keys}.')
    
    # raise warning for unknown keys
    if unknown_keys:
        warnings.warn(f'The following keys are unknown: {unknown_keys}.')

    # TODO: do we want to be able to override?
    # TODO check for .zarr? add .zarr?
    if Path(path).exists():
        raise ValueError(f'File {path} already exists.')

    # create zarr groups
    root = zarr.open(path, mode='w')
    nodes_group = root.create_group('nodes')
    edges_group = root.create_group('edges')
    tracks_group = root.create_group('tracks')

    # add keys 
    for k in data.keys():
        if k not in unknown_keys:
            if Subgroup.get_parent_group(k) == Group.NODES:
                nodes_group.array(name=k, data=data[k])
            elif Subgroup.get_parent_group(k) == Group.EDGES:
                edges_group.array(name=k, data=data[k])
            else:  # Tracks
                tracks_group.array(name=k, data=data[k])


def _validate(data: dict) -> Tuple[list, list]:
    mandatory_keys = Subgroup.get_mandatory_subgroups()
    allowed_keys = Subgroup.list()
    
    # check missing mandatory keys
    missing_keys = [k for k in mandatory_keys if k not in data.keys()]

    # check unknown keys
    unknown_keys = [k for k in data.keys() if k not in allowed_keys]

    # TODO should validate the numpy / pandas values in the dict

    return missing_keys, unknown_keys


def write_parquet(path: Union[str, Path], dataframe: DataFrame):
    table = pa.Table.from_pandas(dataframe)
    pq.write_table(table, path)
