from pathlib import Path

from typing import Any, Union

from pandas import DataFrame
import pyarrow as pa
import pyarrow.parquet as pq

from sequitur.format import FileNames
from sequitur.schema import NodeModel, EdgeModel, GraphModel, TrackModel

ACCEPTED_DTYPES = list[dict[str, Any]] | dict[str, Any] | DataFrame

def write_nodes(
        path: Union[str, Path], 
        nodes: Union[ACCEPTED_DTYPES, list[NodeModel]]
    ):
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
        _write_parquet_df(path / FileNames.NODES.value, nodes_df)
    else:
        if isinstance(nodes[0], NodeModel):
            nodes_list = nodes
        else:
            nodes_list = [
                NodeModel(**node_dict) for node_dict in nodes
            ]

        # write nodes
        _write_parquet_api(path / FileNames.NODES.value, nodes_list)

def write_edges(
        path: Union[str, Path], 
        edges: Union[ACCEPTED_DTYPES, list[EdgeModel]]
    ):
    if isinstance(edges, (dict, DataFrame)):
        edges_df = DataFrame(edges)

        # validate nodes
        required_edge_fields = EdgeModel.required_fields()
        missing_fields = set(required_edge_fields) - set(edges.columns)
        if missing_fields:
            raise ValueError(
                f'Missing required edge fields: {missing_fields}.'
            )
        
        # write out the nodes to file    
        _write_parquet_df(path / FileNames.NODES.value, edges_df)
    else:
        if isinstance(edges[0], EdgeModel):
            edges_list = edges
        else:
            edges_list = [
                EdgeModel(**edge_dict) for edge_dict in edges
            ]

        # write edges
        _write_parquet_api(path / FileNames.EDGES.value, edges_list)


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

def _read_parquet(path: Union[str, Path], **kwargs) -> DataFrame:
    return pq.read_table(path, **kwargs).to_pandas()

def read_nodes(path: Union[str, Path], **kwargs) -> list[NodeModel]:
    dataframe = _read_parquet(path, **kwargs)

    pass

def read_nodes_as_df(path: Union[str, Path], **kwargs) -> DataFrame:
    # TODO check that these are indeed nodes
    return _read_parquet(path, **kwargs)

def read_edges(path: Union[str, Path], **kwargs) -> list[EdgeModel]:
    pass

def read_edges_as_df(path: Union[str, Path], **kwargs) -> DataFrame:
    # TODO check that these are indeed edges
    return _read_parquet(path, **kwargs)

def read_graph(path: Union[str, Path], **kwargs) -> GraphModel:
    pass

def read_tracks(path: Union[str, Path], **kwargs) -> TrackModel:
    pass