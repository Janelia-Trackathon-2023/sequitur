import pandas as pd

from pydantic import BaseModel
from sequitur.schema import NodeModel, EdgeModel, GraphModel, TrackModel
from typing import Any, List, Union


MODELS = Union[NodeModel, EdgeModel, GraphModel, TrackModel]


class SmartModel(BaseModel):
    """This smart model will return the correct model type given the instantiating parameters."""
    model: MODELS

    def required_fields(self):
        fields = [f for f, v in self.model.__fields__.items() if v.required]
        return fields


def validate_df(dataframe: Union[dict[str, List[Any]], pd.DataFrame]) -> type:
    """Validate the columns keys of a dataframe or dict against the required fields of a model."""
    
    # try to infer the model type from the keys in the supplied dictionary or dataframe
    keys = list(dataframe.keys())
    sample_row_dict = {k: dataframe[k][0] for k in keys}

    model = SmartModel(model=sample_row_dict)

    # validate nodes 
    # NOTE: use keys here in case we're passed a dictionary
    required_node_fields = model.required_fields()
    missing_fields = set(required_node_fields) - set(keys)
    if missing_fields:
        raise ValueError(
            f'Missing required node fields: {missing_fields}.'
        )
    
    return type(model.model)
