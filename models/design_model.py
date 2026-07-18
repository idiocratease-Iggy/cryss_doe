from dataclasses import dataclass, field
from typing import List
import pandas as pd

@dataclass
class DesignModel:
    """
    This class acts as the central 'State Container' for the entire application.
    It stores all the data, user selections, and loaded datasets that are 
    shared across different pages of the wizard.
    """
    # File paths for the source Excel data
    solvent_list_filename: str = "SolventList.xlsx"
    descriptor_filename: str = "Descriptors.xlsx"
    salt_former_filename: str = "SaltFormerList.xlsx"

    # User selections from the Solvent Picker and PCA pages
    selected_solvents: List[str] = field(default_factory=list)
    selected_solvents_pca: List[str] = field(default_factory=list)

    # The main chemical descriptor data (loaded from Descriptors.xlsx)
    descriptor_df: pd.DataFrame = field(default_factory=pd.DataFrame)

    # Data regarding salt formers (categorized into acids, bases, etc.)
    salt_former_data: dict = field(default_factory=dict)
    selected_salt_formers: dict = field(default_factory=dict)
    
    # Flag to indicate if a salt-free control set should be included in the design
    include_salt_free_set: bool = False
