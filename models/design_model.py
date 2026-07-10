from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class DesignModel:
    def __init__(self):
            self.selected_solvents = []   # ← important
            self.selected_solvents_pca = []
    number_of_components: int = 0
    number_of_starting_mixtures: int = 0
    selected_solvents: List[str] = None
    selected_salt_formers: List[str] = None
    number_of_volume_levels: int = 0
    volume_mode: str = ""          # "relative" or "absolute"
    replicate_fraction: float = 0.0
    plate_rows: int = 0
    plate_cols: int = 0
    free_format: bool = False
    include_no_salt_set: bool = False
    prefix: str = "EXP"
    timestamp: datetime = datetime.now()
