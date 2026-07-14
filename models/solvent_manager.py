import openpyxl
from utils import normalize

class SolventManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.solvents = []

    def load(self):
        wb = openpyxl.load_workbook(self.filename, data_only=True)
        ws = wb.active

        self.solvents = []

        # Expect a single column: Name
        for row in ws.iter_rows(min_row=2, values_only=True):
            name = row[0]

            if not name:
                continue

            self.solvents.append({
                "Name": normalize(name)
            })
