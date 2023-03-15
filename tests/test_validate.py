from sequitur.validate import validate_df 
from sequitur.schema import NodeModel, EdgeModel, TrackModel


def test_node_validation(example_edges):
    inferred_type = validate_df(example_edges)
    assert issubclass(inferred_type, NodeModel)


def test_edge_validation(example_edges):
    inferred_type = validate_df(example_edges)
    assert issubclass(inferred_type, EdgeModel)


def test_tracks_validation(example_tracks):
    inferred_type = validate_df(example_tracks)
    assert issubclass(inferred_type, TrackModel)