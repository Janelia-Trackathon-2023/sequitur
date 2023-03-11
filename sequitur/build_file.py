from pathlib import Path

import pandas as pd
import numpy as np

class FileBuilder:

    def __init__(self, file: Path) -> None:
        self.file_path = file

    def add_image(data: np.ndarray) -> None:
        pass

    def add_annotations(data: np.ndarray) -> None:
        pass

    def add_edges(data: pd.DataFrame) -> None:
        pass

    def add_nodes(data: pd.DataFrame) -> None:
        pass

    def add_solution(data: pd.DataFrame) -> None:
        pass

    def add_subgraph(nodes: list[int], edges: list[int]) -> None:
        pass

    