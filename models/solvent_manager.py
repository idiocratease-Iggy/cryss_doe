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
