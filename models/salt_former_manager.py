import openpyxl
from utils import normalize
from utils.paths import resource_path

class SaltFormerManager:
    def __init__(self, filename: str):
        self.filename = filename
    
    def load(self):
        # Ensure we look inside the 'data' folder which is bundled by PyInstaller
        file_path = resource_path(f"data/{self.filename}")
        wb = openpyxl.load_workbook(file_path)
    
        # IMPORTANT: select the correct sheet
        ws = wb["SaltFormerList"]   # ← change this to match your sheet name
    
        acids = []
        chiral_acids = []
        bases = []
        chiral_bases = []
    
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row is None:
                continue
    
            acid, chiral_acid, base, chiral_base = row[:4]
    
            if acid:
                acids.append(str(acid).strip())
            if chiral_acid:
                chiral_acids.append(str(chiral_acid).strip())
            if base:
                bases.append(str(base).strip())
            if chiral_base:
                chiral_bases.append(str(chiral_base).strip())
    
        return {
            "acids": acids,
            "chiral_acids": chiral_acids,
            "bases": bases,
            "chiral_bases": chiral_bases,
        }
