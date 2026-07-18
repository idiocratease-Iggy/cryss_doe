import pandas as pd
from utils import normalize

class DescriptorManager:
    """
    Handles the loading and cleaning of chemical descriptor data from Excel files.
    This ensures that the data is consistent (normalized) and complete before 
    being used by the rest of the application.
    """
    def __init__(self, filename: str):
        self.filename = filename
    
    def load(self) -> pd.DataFrame:
        """
        Reads the Excel file, normalizes solvent names, and removes 
        any rows containing missing data.
        """
        df = pd.read_excel(self.filename)
    
        # Normalise solvent names to ensure consistency (e.g., "Ethanol" vs "ethanol")
        if "Solvent" in df.columns:
            df["Solvent"] = df["Solvent"].apply(normalize)
    
        # Remove any rows with empty cells to prevent calculation errors later
        df = df.dropna()
    
        return df
