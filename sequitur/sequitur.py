from pathlib import Path

from typing import Union, Any

import pandas as pd
import numpy as np
import zarr

from numpy import ndarray
from pandas import DataFrame

from sequitur.schema import GraphModel, TrackModel
from sequitur.format import *

class SequiturFile:
    
    def __init__(self, path: Path, mode='r') -> None:
        self._mode = mode if mode == 'w' else 'r'
 
        self._zarr_file = None
        self._has_images = False
        self._has_annotations = False
        self._has_cgraph = False
        self._has_solutions = False
        self._has_tracks = False

        if not path.exists() and mode == 'r':
            raise ValueError(f'File {path} does not exist.')
        elif not path.exists() and mode == 'w':
            path.mkdir(parents=True)
        else:
            # Path exists
            if Path(path, PATH_IMAGE).exists():
                # zarr
                self._zarr_file = zarr.open(Path(path, PATH_IMAGE))
                self._has_images = ZarrGroup.IMAGES in self._zarr_file
                self._has_annotations = ZarrGroup.ANNOTATIONS in self._zarr_file

        # TODO open file if exists
        # TODO check existence of the diverse folder content

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
    def has_candidate_graph(self):
        return self._has_cgraph
    
    @property
    def has_solutions(self):
        return self._has_solutions
    
    @property
    def has_tracks(self):
        return self._has_tracks
    
    def get_image(self) -> ndarray:
        pass

    def get_annotations(self) -> ndarray:
        pass

    def get_candidate_graph(self) -> list[DataFrame]:
        pass
    
    def get_solutions(self) -> list[tuple[DataFrame]]:
        pass

    def get_tracks(self) -> list[DataFrame]:
        pass

    def add_image(self, array: ndarray) -> None:
        if self.mode == 'w':
            pass

    def copy_image(self, path_to_zarr: Union[str, Path]) -> None:
        if self.mode == 'w':
            pass

    def add_annotations(self, array: ndarray) -> None:
        if self.mode == 'w':
            pass

    def copy_annotations(self, path_to_zarr: Union[str, Path]) -> None:
        if self.mode == 'w':
            pass

    # TODO typing
    def add_candidate_graph(self, nodes, edges=None) -> None:
        if self.mode == 'w':
            pass

    # TODO typing
    def add_solution(self, nodes, edges) -> None:
        if self.mode == 'w':
            pass

    # TODO typing
    def add_tracks(self, nodes, edges) -> None:
        if self.mode == 'w':
            pass


def open(path: Union[str, Path], mode='r'):
    return SequiturFile(path=path, mode=mode)