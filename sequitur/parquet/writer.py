from pathlib import Path

from typing import Any, Union

from pandas import DataFrame
import pyarrow as pa
import pyarrow.parquet as pq

ACCEPTED_DATATYPES = dict[str, Any] | DataFrame

def write(path: Union[str, Path], nodes: ACCEPTED_DATATYPES, edges: ACCEPTED_DATATYPES) -> None:
    """Write out a graph."""

    path = Path(path)

    if not Path(path).is_dir():
        raise ValueError("Supplied path must be a directory.")

    # TODO: validate the incoming data
    if isinstance(nodes, dict):
        nodes = DataFrame(nodes)
    
    if isinstance(edges, dict):
        edges = DataFrame(edges)

    # TODO define path in format
    _write_parquet(path / "nodes.parquet", nodes)
    _write_parquet(path / "edges.parquet", edges)


def _write_parquet(path: Union[str, Path], dataframe: DataFrame):
    table = pa.Table.from_pandas(dataframe)
    pq.write_table(table, path)