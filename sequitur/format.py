from __future__ import annotations
from enum import Enum
from typing import List

# TODO: is there an alternative to Enums?

class FileNames(str, Enum):
    ZARR = 'images.zarr'
    EDGES = 'edges.parquet'
    NODES = 'nodes.parquet'

class ZarrGroup(str, Enum):
    IMAGES = 'images'
    ANNOTATIONS = 'annotations'

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