from typing import List, Tuple, Optional
from pydantic import BaseModel, root_validator


class NodeModel(BaseModel):
    id: int
    pos: Tuple[float]  # can be an empty tuple
    score: Optional[float] = None

    class Config:
        extra = "allow"


class EdgeModel(BaseModel):
    id: int
    src_id: int
    dst_id: int
    score: Optional[float] = None

    class Config:
        extra = "allow"


class GraphModel(BaseModel):
    nodes: List[NodeModel]
    edges: List[EdgeModel]
    axis_order: Tuple[str]  # can be an empty tuple

    @root_validator
    def validate(cls, values):
        nodes = values.get("nodes")
        edges = values.get("edges")
        axis_order = values.get("axis_order")
        for node in nodes:
            if len(node.pos) != len(axis_order):
                raise ValueError
        node_ids = set(node.id for node in nodes)
        edge_node_set = set(edge.src_id for edge in edges).union(
            set(edge.dst_id for edge in edges)
        )
        if not edge_node_set.issubset(node_ids):
            raise ValueError


class TrackModel(GraphModel):
    id: int
    start_id: int
    end_id: int

    class Config:
        extra = "allow"
