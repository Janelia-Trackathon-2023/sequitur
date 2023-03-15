from pathlib import Path

from typing import Union, Any

import pandas as pd
import numpy as np
import zarr

from numpy import ndarray
from pandas import DataFrame

from sequitur.format import *
from sequitur.parquet.parquet_io import read_df

class SequiturFile:
    
    def __init__(self, path: Path, mode='r') -> None:
        self._mode = mode if mode == 'w' else 'r'
        self._path = path
 
        self._zarr_file = None
        self._has_images = False
        self._has_annotations = False
        self._has_nodes = False
        self._has_edges = False
        self._has_solution = False
        self._has_tracks = False

        if not path.exists() and mode == 'r':
            raise ValueError(f'File {path} does not exist.')
        elif not path.exists() and mode == 'w':
            path.mkdir(parents=True)
        else:
            # Path exists, check if it contains the zarr
            if Path(path, PATH_IMAGE).exists():
                # zarr
                self._zarr_file = zarr.open(Path(path, PATH_IMAGE))
                self._has_images = ZarrGroup.IMAGES in self._zarr_file
                self._has_annotations = ZarrGroup.ANNOTATIONS in self._zarr_file

            # Candidate graph
            if Path(path, PATH_GRAPH).exists():
                # nodes
                self._has_nodes = Path(path, PATH_NODES).exists() 

                # edges
                # TODO support for multiple subgraphs
                self._has_edges =  Path(path, PATH_EDGES).exists() 

                # solution
                # TOOD what to do with the solution nodes and edges here?
                self._has_solution =  Path(path, PATH_SOLUTION_EDGES).exists() 

                # tracks
                self._has_tracks =  Path(path, PATH_TRACKS).exists() 

                # TODO: change this, solutions and tracks require edges as well
                if not self._has_nodes:
                    if self._has_edges or self._has_solution or self.has_tracks:
                        raise ValueError(
                            'Broken graph: edges, solution or tracks cannot exist without nodes.'
                        )
            

    @property
    def mode(self):
        return self._mode

    @property
    def has_images(self):
        return self._has_images
    
    @property
    def has_annotations(self):
        return self._has_annotations
    
    @property
    def has_nodes(self):
        return self._has_nodes

    @property
    def has_edges(self):
        return self._has_edges
    
    @property
    def has_solution(self):
        return self._has_solution
    
    @property
    def has_tracks(self):
        return self._has_tracks
    
    def read_image(self) -> ndarray:
        if self.has_images:
            return self._zarr_file[ZarrGroup.IMAGES]

    def read_annotations(self) -> ndarray:
        if self.has_annotations:
            return self._zarr_file[ZarrGroup.ANNOTATIONS]

    def read_nodes(self) -> DataFrame:
        if self.has_nodes:
            return read_df(Path(self._path, PATH_NODES))
    
    def read_edges(self) -> DataFrame:
        if self.has_edges:
            return read_df(Path(self._path, PATH_EDGES))
    
    def read_solution(self) -> list[tuple[DataFrame]]:
        pass

    def read_tracks(self) -> list[DataFrame]:
        pass

    def write_image(self, array: ndarray) -> None:
        if self.mode == 'w':
            pass

    def copy_image(self, path_to_zarr: Union[str, Path]) -> None:
        if self.mode == 'w':
            pass

    def write_annotations(self, array: ndarray) -> None:
        if self.mode == 'w':
            pass

    def copy_annotations(self, path_to_zarr: Union[str, Path]) -> None:
        if self.mode == 'w':
            pass

    # TODO typing
    def write_nodes(self, nodes) -> None:
        if self.mode == 'w':
            pass

    def write_edges(self, edges) -> None:
        if self.mode == 'w':
            pass

    # TODO typing
    def write_solution(self, nodes, edges) -> None:
        if self.mode == 'w':
            pass

    # TODO typing
    def write_tracks(self, nodes, edges) -> None:
        if self.mode == 'w':
            pass


def open(path: Union[str, Path], mode='r'):
    return SequiturFile(path=path, mode=mode)