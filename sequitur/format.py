from __future__ import annotations
from pathlib import Path

from enum import Enum
from typing import List

# TODO: is there an alternative to Enums?



class FileNames(str, Enum):
    MAIN = 'sequitur.file'
    ZARR = 'images.zarr'
    EDGES = 'edges.parquet'
    NODES = 'nodes.parquet'
    SOLUTION = 'solution.parquet'
    TRACKS = 'tracks.parquet'

class ZarrGroup(str, Enum):
    IMAGES = 'images'
    ANNOTATIONS = 'annotations'

PATH_IMAGE = Path(FileNames.MAIN, FileNames.ZARR)
PATH_GRAPH = Path(FileNames.MAIN, 'graph')
PATH_EDGES = Path(FileNames.MAIN, 'graph', 'edges', FileNames.EDGES)
PATH_NODES = Path(FileNames.MAIN, 'graph', 'nodes', FileNames.NODES)
PATH_SOLUTION = Path(FileNames.MAIN, 'solution', 'solution', FileNames.SOLUTION)
PATH_NODES = Path(FileNames.MAIN, 'graph', 'tracks', FileNames.TRACKS)

class NodeEntries(str, Enum):
    ID = 'node_id'
    COORDINATES = 'coordinates'
    SCORE = 'score'

    @staticmethod
    def get_mandatory_fields() -> list[str]:
        return [
            NodeEntries.ID,
            NodeEntries.COORDINATES
        ]

class EdgeEntries(str, Enum):
    ID = 'edge_id'
    SOURCE = 'source_id'
    TARGET = 'target_id'
    SCORE = 'score'

    @staticmethod
    def get_mandatory_fields() -> list[str]:
        return [
            EdgeEntries.ID,
            EdgeEntries.SOURCE,
            EdgeEntries.TARGET
        ]

class GraphEntries(str, Enum):
    NODES = 'nodes'
    EDGES = 'edges'

class Subgraph(str, Enum):
    SOLUTION = 'solution'
    GT = 'ground-truth'


class TrackEntries(str, Enum):
    ID = 'track_id'
    START = 'start_id'
    END = 'end_id'