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
    ID = 'nid'
    COORDINATES = 'coordinates'
    SCORE = 'score'

    @staticmethod
    def get_mandatory_fields() -> list[str]:
        return [
            NodeEntries.ID.value,
            NodeEntries.COORDINATES.value
        ]

class EdgeEntries(str, Enum):
    ID = 'eid'
    SOURCE = 'source'
    TARGET = 'target'
    SCORE = 'score'

    @staticmethod
    def get_mandatory_fields() -> list[str]:
        return [
            EdgeEntries.ID.value,
            EdgeEntries.SOURCE.value,
            EdgeEntries.TARGET.value
        ]

class GraphEntries(str, Enum):
    NODES = 'nodes'
    EDGES = 'edges'

class Subgraph(str, Enum):
    SOLUTION = 'solution'
    GT = 'ground-truth'