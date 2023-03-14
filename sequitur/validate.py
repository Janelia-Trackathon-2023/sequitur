import pandas as pd

from schema import NodeModel, EdgeModel, GraphModel, TrackModel
from typing import Any, List, Union


MODELS = Union[NodeModel, EdgeModel, GraphModel, TrackModel]


def validate_df_keys(model: MODELS, dataframe: Union[dict[str, List[Any]], pd.DataFrame]) -> None:
    """Validate the columns keys of a dataframe or dict against the required fields of a model."""
    
    if not issubclass(model, MODELS):
        raise TypeError("`model` needs to be a recognised `Model`")

    # validate nodes 
    # NOTE: use keys here in case we're passed a dictionary
    required_node_fields = model.required_fields()
    missing_fields = set(required_node_fields) - set(dataframe.keys())
    if missing_fields:
        raise ValueError(
            f'Missing required node fields: {missing_fields}.'
        )


foo = {"node_id": [], "bar": [], "coordinates": []}
validate_df_keys(NodeModel, foo)