import openpyxl


class SolventManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.solvents = []
        self.n_rows = 0  # <-- IMPORTANT: define it here

    def load(self):
        wb = openpyxl.load_workbook(self.filename)
        ws = wb.active

        # Read header row
        headers = [cell.value for cell in ws[1]]

        # Count rows excluding header
        self.n_rows = ws.max_row - 1

          # Load solvent entries
        for row in ws.iter_rows(min_row=2, values_only=True):
                   if any(val is not None and str(val).strip() != "" for val in row):
                       entry = dict(zip(headers, row))
                       self.solvents.append(entry)
