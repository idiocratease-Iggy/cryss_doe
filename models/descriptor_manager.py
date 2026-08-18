# MIT License
#
# Copyright (c) [2026] [Alan A. Smith]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pandas as pd
from utils import normalize
from utils.paths import resource_path

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
        # Ensure we look inside the 'data' folder which is bundled by PyInstaller
        file_path = resource_path(f"data/{self.filename}")
        df = pd.read_excel(file_path)
    
        # Normalise solvent names to ensure consistency (e.g., "Ethanol" vs "ethanol")
        if "Solvent" in df.columns:
            df["Solvent"] = df["Solvent"].apply(normalize)
    
        # Remove any rows with empty cells to prevent calculation errors later
        df = df.dropna()
    
        return df
