from __future__ import annotations
from enum import Enum
from typing import List

class FileNames(Enum):
    ZARR = 'images.zarr'
    EDGES = 'edges.parquet'
    NODES = 'nodes.parquet'

class ZarrGroup(Enum):
    IMAGES = 'images'
    ANNOTATIONS = 'annotations'

class NodeEntries(Enum):
    ID = 'nid'
    COORDINATES = 'coordinates'
    SCORE = 'score'

class EdgeEntries(Enum):
    ID = 'eid'
    SOURCE = 'source'
    TARGET = 'target'
    SCORE = 'score'

class GraphEntries(Enum):
    NODES = 'nodes'
    EDGES = 'edges'