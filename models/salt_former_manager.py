import openpyxl

class SaltFormerManager:
    def __init__(self, filename: str):
        self.filename = filename

    def load(self):
        wb = openpyxl.load_workbook(self.filename)
        print("Workbook sheets:", wb.sheetnames)

        # IMPORTANT: select the correct sheet
        ws = wb["SaltFormerList"]   # ← change this to match your sheet name

        print("Active sheet title:", ws.title)
        print("Max row:", ws.max_row)
        print("Max column:", ws.max_column)

        acids = []
        chiral_acids = []
        bases = []
        chiral_bases = []

        for row in ws.iter_rows(min_row=2, values_only=True):
            print("Row read:", row)

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
