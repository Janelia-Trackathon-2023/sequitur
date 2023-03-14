from pathlib import Path

from typing import Any, Union

from pandas import DataFrame
import pyarrow as pa
import pyarrow.parquet as pq

from sequitur.format import FileNames
from sequitur.schema import NodeModel, EdgeModel

ACCEPTED_DTYPES = list[dict[str, Any]] | dict[str, Any] | DataFrame

def write_parquet(
        path: Union[str, Path], 
        nodes: Union[ACCEPTED_DTYPES, list[NodeModel]], 
        edges: Union[ACCEPTED_DTYPES, list[EdgeModel]] = None
    ) -> None:
    """Write out a graph."""

    # TODO validate path
    path = Path(path)
    if not path.exists():
        path.mkdir(parents=True)

    # TODO check that node and edges are compatible types

    # TODO: validate the incoming data
    if isinstance(nodes, (dict, DataFrame)):
        nodes_df = DataFrame(nodes)

        # validate nodes
        required_node_fields = NodeModel.required_fields()
        missing_fields = set(required_node_fields) - set(nodes.columns)
        if missing_fields:
            raise ValueError(
                f'Missing required node fields: {missing_fields}.'
            )
        
        # write out the nodes to file    
        _write_parquet_df(path / FileNames.NODES.value, nodes)
        
        if edges is not None:
            if isinstance(edges, dict):
                edges_df = DataFrame(edges)
            else:
                raise ValueError(
                    'Nodes and edges should be of the same type '
                    f'(here {type(nodes)} and {type(edges)}).'
                )

            required_edge_fields = EdgeModel.required_fields()
            missing_fields = set(required_edge_fields) - set(edges.columns)
            if missing_fields:
                raise ValueError(
                    f'Missing required edges fields: {missing_fields}.'
                )


    _write_parquet_df(path / FileNames.NODES.value, nodes)
    _write_parquet_df(path / FileNames.EDGES.value, edges)


def _write_parquet_api(path: Union[str, Path], data: list):
    fields = data[0].__fields__.keys()

    table = {}
    for f in fields:
        table.update(
            {
                f: [getattr(item, f) for item in data]
            }
        )

    _write_parquet_df(path, DataFrame.from_dict(table))
    

def _write_parquet_df(path: Union[str, Path], dataframe: DataFrame):
    table = pa.Table.from_pandas(dataframe)
    pq.write_table(table, path)


def read_parquet(path: Union[str, Path], **kwargs):
    return pq.read_table(path, **kwargs)