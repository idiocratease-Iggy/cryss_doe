from dataclasses import dataclass, field
from typing import List, Dict, Optional
import pandas as pd

@dataclass
class DesignModel:
    """
    Central state container for the entire DoE wizard.
    All pages write their values into this model.
    """
    
    # -----------------------------
    # File paths
    # -----------------------------
    solvent_list_filename: str = "SolventList.xlsx"
    descriptor_filename: str = "Descriptors.xlsx"
    salt_former_filename: str = "SaltFormerList.xlsx"

    # -----------------------------
    # Loaded data
    # -----------------------------
    descriptor_df: pd.DataFrame = field(default_factory=pd.DataFrame)
    salt_former_data: Dict = field(default_factory=dict)

    # -----------------------------
    # User selections
    # -----------------------------
    selected_solvents: List[str] = field(default_factory=list)
    selected_solvents_pca: List[str] = field(default_factory=list)
    selected_salt_formers: List[str] = field(default_factory=list)

    number_of_volume_levels: int = 2
    volume_mode: str = "relative"
    volume_unit: Optional[str] = None

    number_of_starting_mixtures: int = 0

    include_salt_free_set: bool = False

    # -----------------------------
    # Plate design
    # -----------------------------
    plate_rows: int = 0
    plate_cols: int = 0
    fill_to_full_plates: bool = False
    free_format: bool = False

    # -----------------------------
    # Replicates & randomization
    # -----------------------------
    replicate_percentage: float = 0.0
    randomize_design: bool = False

    # -----------------------------
    # Output
    # -----------------------------
    output_filename: str = "experiment_output.xlsx"
