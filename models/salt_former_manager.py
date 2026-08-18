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
