from __future__ import annotations
from enum import Enum
from typing import List

# TODO store data, candidate graphs, multiple solutions
# TODO tie a solution to a candidate graph?
# TODO use schema to specify types?

class Group(Enum):
    NODES = 'nodes'
    EDGES = 'edges'
    TRACKS = 'tracks'


class Subgroup(Enum):
    NODES_ID = 'nid'
    NODES_T = 't'

    # keep x and y explicit to avoid xy vs yx
    NODES_X = 'x'
    NODES_Y = 'y'

    NODES_Z = 'z'

    EDGES_ID = 'eid'
    EDGES_SOURCE = 'source'
    EDGES_TARGET = 'target'

    TRACKS_ID = 'tid'
    TRACKS_BEGIN = 'begin'
    TRACKS_END = 'end'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @staticmethod
    def get_mandatory_subgroups() -> list:
        return [
            Subgroup.NODES_ID.value,
            Subgroup.NODES_T.value,
            Subgroup.NODES_X.value,

            Subgroup.EDGES_ID.value,
            Subgroup.EDGES_SOURCE.value,
            Subgroup.EDGES_TARGET.value,      
        ]

    @staticmethod
    def get_parent_group(subgroup: str) -> Group:
        if subgroup in Subgroup._get_node_subgroups():
            return Group.NODES
        elif subgroup in Subgroup._get_edge_subgroups():
            return Group.EDGES
        # TODO this will change if additional groups are added
        else:
            return Group.TRACKS

    @staticmethod
    def _get_node_subgroups() -> List[Subgroup]:
        return [
            Subgroup.NODES_ID.value,
            Subgroup.NODES_T.value,
            Subgroup.NODES_Z.value,
            Subgroup.NODES_X.value,
            Subgroup.NODES_Y.value,
        ]

    @staticmethod
    def _get_edge_subgroups() -> List[Subgroup]:
        return [
            Subgroup.EDGES_ID.value,
            Subgroup.EDGES_SOURCE.value,
            Subgroup.EDGES_TARGET.value,
        ]