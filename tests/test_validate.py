from sequitur.validate import validate_df 
from sequitur.schema import NodeModel, EdgeModel, TrackModel


def test_node_validation(simple_nodes):
    inferred_type = validate_df(simple_nodes)
    assert issubclass(inferred_type, NodeModel)


def test_edge_validation(simple_edges):
    inferred_type = validate_df(simple_edges)
    assert issubclass(inferred_type, EdgeModel)


def test_tracks_validation(simple_tracks):
    inferred_type = validate_df(simple_tracks)
    assert issubclass(inferred_type, TrackModel)