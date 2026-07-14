import pandas as pd
from utils import normalize

class DescriptorManager:
    def __init__(self, filename: str):
        self.filename = filename

    def load(self) -> pd.DataFrame:
        df = pd.read_excel(self.filename)

        # Normalise solvent names
        if "Solvent" in df.columns:
            df["Solvent"] = df["Solvent"].apply(normalize)

        # Drop rows with missing values
        df = df.dropna()

        return df
