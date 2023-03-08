from enum import Enum

# TODO use schema to specify types?

class Groups(Enum):
    NODES_ID = 'nid'
    NODES_T = 't'
    NODES_Z = 'z'
    NODES_X = 'x'
    NODES_Y = 'y'

    EDGES_ID = 'eid'
    EDGES_SOURCE = 'source'
    EDGES_target = 'target'

    TRACKS_ID = 'tid'
    TRACKS_BEGIN = 'begin'
    TRACKS_END = 'end'

