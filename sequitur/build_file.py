from pathlib import Path

import pandas as pd
import numpy as np

from sequitur.format import NodeEntries, EdgeEntries, FileNames
from sequitur.parquet.parquet_io import write_parquet
from sequitur.zarr.zarr_io import write_zarr

class FileBuilder:

    def __init__(self, file: Path) -> None:
        # TODO check path?
        self.file_path = file

    # TODO: should have the possibility to copy a zarr?
    def add_images(
            self, 
            images: np.ndarray,
            annotations: np.ndarray
        ) -> None:
        path = Path(self.file_path, FileNames.ZARR.value)

        write_zarr(path, images, annotations)

    def add_graph(
            self, 
            nodes: pd.DataFrame, 
            edges: pd.DataFrame
        ) -> None:
        # check mandatory fields
        missing_node_fields = [
            f for f in NodeEntries.get_mandatory_fields() if f not in nodes.keys()
        ]
        if not missing_node_fields:
            raise ValueError(f'Missing the following node fields: {missing_node_fields}')
        
        missing_edge_fields = [
            f for f in EdgeEntries.get_mandatory_fields() if f not in nodes.keys()
        ]
        if not missing_edge_fields:
            raise ValueError(f'Missing the following edge fields: {missing_edge_fields}')

        # TODO check that coordinate field is a list of tuple
        write_parquet(self.file_path, nodes, edges)
        
    def add_solution(self, data: pd.DataFrame) -> None:
        pass

    def add_subgraph(self, nodes: list[int], edges: list[int]) -> None:
        pass

    