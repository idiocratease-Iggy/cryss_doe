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

from PyQt6.QtWidgets import (
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QWizardPage,
)


class PageStartingMixtures(QWizardPage):
    def __init__(self, design_model):
        super().__init__()
        self.design = design_model
        self.setTitle("Number of Starting Mixtures")

        layout = QVBoxLayout()

        label = QLabel(
            "Specify how many Starting Mixtures (SMs) you want.\n"
            "Each SM will later have its own composition (Component1..N) "
            "in the template. The DoE module only needs the count."
        )

        self.spin = QSpinBox()
        self.spin.setMinimum(1)
        self.spin.setMaximum(20)  # adjustable
        self.spin.setValue(1)  # default: 1 SM
        self.spin.valueChanged.connect(self._on_value_changed)
        

        layout.addWidget(label)
        layout.addWidget(self.spin)
        self.setLayout(layout)


    def _on_value_changed(self, value: int):
        self.design.number_of_starting_mixtures = value

    def validatePage(self) -> bool:
        value = self.spin.value()
        if value < 1:
            return False
        self.design.number_of_starting_mixtures = value
        return True
