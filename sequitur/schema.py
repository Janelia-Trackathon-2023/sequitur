from typing import Any, List, Tuple, Optional
from pydantic import BaseModel, root_validator


class FloatTuple(List[float]):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, values: List[float]):
        return tuple(float(v) for v in values)


class StrTuple(List[str]):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, values: List[str]):
        return tuple(str(v) for v in values)


class NodeModel(BaseModel):
    node_id: int
    # coordinates: FloatTuple  # can be an empty tuple
    score: Optional[float] = None

    class Config:
        extra = "allow"


class EdgeModel(BaseModel):
    edge_id: int
    source_id: int
    target_id: int
    score: Optional[float] = None

    class Config:
        extra = "allow"


class GraphModel(BaseModel):
    nodes: List[NodeModel]
    edges: List[EdgeModel]
    axis_order: StrTuple  # can be an empty tuple

    # TODO(arl): need to get this working!
    @root_validator
    def validate(cls, values):
        nodes = values.get("nodes")
        edges = values.get("edges")
        axis_order = values.get("axis_order")
        for node in nodes:
            if len(node.coordinates) != len(axis_order):
                raise ValueError
        node_ids = set(node.node_id for node in nodes)
        edge_node_set = set(edge.source_id for edge in edges).union(
            set(edge.target_id for edge in edges)
        )
        if not edge_node_set.issubset(node_ids):
            raise ValueError
        return values


class TrackModel(BaseModel):
    track_id: int
    start_id: int
    end_id: int

    class Config:
        extra = "allow"
