from pathlib import Path

from typing import Union, Any

import pandas as pd
import numpy as np
import zarr

from numpy import ndarray
from pandas import DataFrame

from sequitur.format import *
from sequitur.parquet.parquet_io import read_df, write_df

class SequiturFile:
    
    def __init__(self, path: Union[str, Path], mode='r') -> None:
        self._mode = mode if mode == 'w' else 'r'
        self._path = Path(path)
 
        self._zarr_file = None
        self._has_images = False
        self._has_annotations = False
        self._has_nodes = False
        self._has_edges = False
        self._has_solution = False
        self._has_tracks = False

        if not self._path.exists() and mode == 'r':
            raise ValueError(f'File {self._path} does not exist.')
        elif not self._path.exists() and mode == 'w':
            self._path.mkdir(parents=True)
        else:
            # Path exists, check if it contains the zarr
            if Path(self._path, PATH_IMAGE).exists():
                # zarr
                # TODO: this opens the zarr, what is the overhead?
                self._zarr_file = zarr.open(Path(self._path, PATH_IMAGE))
                self._has_images = ZarrGroup.IMAGES.value in self._zarr_file
                self._has_annotations = ZarrGroup.ANNOTATIONS.value in self._zarr_file

            # Candidate graph
            if Path(self._path, PATH_GRAPH).exists():
                # nodes
                self._has_nodes = Path(self._path, PATH_NODES).exists() 

                # edges
                # TODO support for multiple subgraphs
                self._has_edges =  Path(self._path, PATH_EDGES).exists() 

                # solution
                # TOOD what to do with the solution nodes and edges here?
                self._has_solution =  Path(self._path, PATH_SOLUTION_EDGES).exists() 

                # tracks
                self._has_tracks =  Path(self._path, PATH_TRACKS).exists() 

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
            return self._zarr_file[ZarrGroup.IMAGES.value][:]

    def read_annotations(self) -> ndarray:
        if self.has_annotations:
            return self._zarr_file[ZarrGroup.ANNOTATIONS.value][:]

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
            if self._zarr_file is None:
                self._zarr_file = zarr.open(Path(self._path, PATH_IMAGE))
                
            # TODO better way to do zarr?
            if self._has_images:
                # TODO here we can have dimension and chunk problems
                self._zarr_file[ZarrGroup.IMAGES.value] = array
            else:
                self._zarr_file.array(name=ZarrGroup.IMAGES.value, data=array)
            
            self._has_images = True

    # TODO
    def copy_image(self, path_to_zarr: Union[str, Path]) -> None:
        if self.mode == 'w':
            pass

    def write_annotations(self, array: ndarray) -> None:
        if self.mode == 'w':
            if self._zarr_file is None:
                self._zarr_file = zarr.open(Path(self._path, PATH_IMAGE))
                
            # TODO better way to do zarr?
            if self._has_images:
                # TODO here we can have dimension and chunk problems
                self._zarr_file[ZarrGroup.ANNOTATIONS.value] = array
            else:
                self._zarr_file.array(name=ZarrGroup.ANNOTATIONS.value, data=array)
            
            self._has_annotations = True

    # TODO
    def copy_annotations(self, path_to_zarr: Union[str, Path]) -> None:
        if self.mode == 'w':
            pass

    # TODO typing
    def write_nodes(self, nodes: DataFrame) -> None:
        if self.mode == 'w':
            write_df(Path(self._path, PATH_NODES), nodes)
            self._has_nodes = True

    def write_edges(self, edges: DataFrame) -> None:
        if self.mode == 'w':
            write_df(Path(self._path, PATH_EDGES), edges)
            self._has_edges = True

    # TODO typing
    def write_solution(self, nodes, edges) -> None:
        if self.mode == 'w':
            pass

    # TODO typing
    def write_tracks(self, nodes, edges) -> None:
        if self.mode == 'w':
            pass

    # TODO remove functions?

def open(path: Union[str, Path], mode='r'):
    return SequiturFile(path=path, mode=mode)