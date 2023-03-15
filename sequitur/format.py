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

# TODO: frozen dataclass with those as fields 
PATH_IMAGE = Path(FileNames.ZARR)
PATH_GRAPH = Path('graph')
PATH_NODES = Path('graph', 'nodes', FileNames.NODES)
PATH_EDGES = Path('graph', 'subgraph', 'edges', FileNames.EDGES)
PATH_SOLUTION = Path('graph', 'subgraph', 'solution', FileNames.SOLUTION)
PATH_TRACKS = Path('graph', 'subgraph', 'tracks', FileNames.TRACKS)

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