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


def _write_parquet_api(
        path: Union[str, Path], 
        data: list[Union[NodeModel, EdgeModel]]
    ):
    # read node or edge fields
    fields = data[0].__fields__.keys()

    # create a dataframe compatible dict
    table = {}
    for f in fields:
        table.update(
            {
                f: [getattr(item, f) for item in data]
            }
        )

    # convert to dataframe and write to disk
    _write_parquet_df(path, DataFrame.from_dict(table))
    

def _write_parquet_df(path: Union[str, Path], dataframe: DataFrame):
    table = pa.Table.from_pandas(dataframe)
    pq.write_table(table, path)

def _read_parquet_df(path: Union[str, Path], **kwargs) -> DataFrame:
    return pq.read_table(path, **kwargs).to_pandas()

def read_nodes(path: Union[str, Path], **kwargs) -> list[NodeModel]:
    nodes_as_dict = _read_parquet_df(path, **kwargs).to_dict(orient='records')

    # TODO: used class from validation?
    nodes_lst = []
    for entry in nodes_as_dict:
        nodes_lst.append(
            NodeModel(**entry)
        )
    
    return nodes_lst

def read_nodes_as_df(path: Union[str, Path], **kwargs) -> DataFrame:
    # TODO check that these are indeed nodes
    return _read_parquet_df(path, **kwargs)

def read_edges(path: Union[str, Path], **kwargs) -> list[EdgeModel]:
    edges_as_dict = _read_parquet_df(path, **kwargs).to_dict(orient='records')

    # TODO: used class from validation?
    edges_lst = []
    for entry in edges_as_dict:
        edges_lst.append(
            EdgeModel(**entry)
        )
    
    return edges_lst

def read_edges_as_df(path: Union[str, Path], **kwargs) -> DataFrame:
    # TODO check that these are indeed edges
    return _read_parquet_df(path, **kwargs)


def read_graph(
        node_path: Union[str, Path],
        edge_path: Union[str, Path], 
        **kwargs
    ) -> GraphModel:
    # TODO how to deal with the path here? need relative path for 
    # edges and nodes

    # TODO read metadata for axis order

    nodes = read_nodes(node_path)
    edges = read_edges(edge_path)

    return GraphModel(
        nodes=nodes,
        edges=edges,
        axis_order=('?',)
    )


def read_tracks(path: Union[str, Path], **kwargs) -> TrackModel:
    pass