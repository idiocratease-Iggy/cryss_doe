from dataclasses import dataclass, field
from typing import List
import pandas as pd

@dataclass
class DesignModel:
    solvent_list_filename: str = "SolventList.xlsx"
    descriptor_filename: str = "Descriptors.xlsx"

    selected_solvents: List[str] = field(default_factory=list)
    selected_solvents_pca: List[str] = field(default_factory=list)

    descriptor_df: pd.DataFrame = field(default_factory=pd.DataFrame)
