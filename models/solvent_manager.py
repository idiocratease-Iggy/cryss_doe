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

import openpyxl
from utils import normalize
from utils.paths import resource_path

class SolventManager:
    """
    Handles loading the master list of solvents from an Excel file.
    This provides the base list of chemicals that users can choose from 
    in the wizard.
    """
    def __init__(self, filename: str):
        self.filename = filename
        self.solvents = []
    
    def load(self):
        """
        Opens the Excel workbook and extracts solvent names into a list.
        Uses 'data_only=True' to ensure we get values instead of formulas.
        """
        # Ensure we look inside the 'data' folder which is bundled by PyInstaller
        file_path = resource_path(f"data/{self.filename}")
        # Load the workbook, ensuring we read the resulting values of any formulas
        wb = openpyxl.load_workbook(file_path, data_only=True)
        ws = wb.active
    
        self.solvents = []
    
        # Iterate through rows (skipping header) to build a list of solvent dictionaries
        for row in ws.iter_rows(min_row=2, values_only=True):
            name = row[0]
    
            if not name:
                continue
    
            self.solvents.append({
                "Name": normalize(name)
            })
