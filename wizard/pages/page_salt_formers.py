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
    QWizardPage,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox,
    QCheckBox,
    QScrollArea,
    QWidget,
    QFrame,
)

from PyQt6.QtCore import Qt


class PageSaltFormers(QWizardPage):
    def __init__(self, design_model):
        super().__init__()
        self.setTitle("Select Salt Formers")

        self.design = design_model
        self.setTitle("Salt Formers (Optional)")

        # 1. Load salt former data from the model
        data = self.design.salt_former_data
        acids = data["acids"]
        chiral_acids = data["chiral_acids"]
        bases = data["bases"]
        chiral_bases = data["chiral_bases"]

        # 2. Ensure model has fields
        if not hasattr(self.design, "selected_salt_formers"):
            self.design.selected_salt_formers = {
                "acids": [],
                "chiral_acids": [],
                "bases": [],
                "chiral_bases": [],
            }

        if not hasattr(self.design, "include_salt_free_set"):
            self.design.include_salt_free_set = False

        # 3. Build the UI layout
        main_layout = QVBoxLayout()

        info_label = QLabel(
            "Salt formers are optional.\n"
            "You may skip this page if not applicable."
        )
        main_layout.addWidget(info_label)

        # 4. Build the four columns using the lists loaded above
        columns_layout = QHBoxLayout()

        self.acid_checkboxes = []
        self.chiral_acid_checkboxes = []
        self.base_checkboxes = []
        self.chiral_base_checkboxes = []

        def build_group(title, items, store_list):
            box = QGroupBox(title)
            v = QVBoxLayout()
            for item in items:
                 cb = QCheckBox(item)
                 font = cb.font()
                 font.setPointSize(9)
                 cb.setFont(font)
                 cb.setStyleSheet("font-size: 9pt;")
                 cb.stateChanged.connect(self.update_salt_free_visibility)
                 store_list.append(cb)
                 v.addWidget(cb)
            v.addStretch()
            box.setLayout(v)
            return box

        columns_layout.addWidget(build_group("Acids", acids, self.acid_checkboxes))
        columns_layout.addWidget(build_group("Chiral Acids", chiral_acids, self.chiral_acid_checkboxes))
        columns_layout.addWidget(build_group("Bases", bases, self.base_checkboxes))
        columns_layout.addWidget(build_group("Chiral Bases", chiral_bases, self.chiral_base_checkboxes))

        # Wrap columns in a scroll area to prevent clipping on small screens
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.setSpacing(0)
        container_layout.addLayout(columns_layout)
        container_layout.addStretch()
        
        scroll.setWidget(container)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #3c3c3c;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #718096;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar:horizontal {
                border: none;
                background: #3c3c3c;
                height: 10px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #718096;
                min-width: 20px;
                border-radius: 5px;
            }
        """)
        main_layout.addWidget(scroll)





        # 5. Salt-free checkbox (hidden until needed)
        self.salt_free_checkbox = QCheckBox("Include a salt-free set")
        self.salt_free_checkbox.setVisible(False)
        main_layout.addWidget(self.salt_free_checkbox)

        self.setLayout(main_layout)




    def update_salt_free_visibility(self):
        """Show the salt-free checkbox if any salt former is selected."""
        any_selected = (
            any(cb.isChecked() for cb in self.acid_checkboxes) or
            any(cb.isChecked() for cb in self.chiral_acid_checkboxes) or
            any(cb.isChecked() for cb in self.base_checkboxes) or
            any(cb.isChecked() for cb in self.chiral_base_checkboxes)
        )

        self.salt_free_checkbox.setVisible(any_selected)

    def showEvent(self, event):
        super().showEvent(event)
        # Call the helper method you already wrote!
        self.update_salt_free_visibility()
        wizard = self.wizard()
        if wizard is not None:
            # Set standard dimensions for the wizard window
            wizard.setMinimumSize(600, 500)   # ⭐ critical
            wizard.resize(600, 500)
    
            # Center the window on the user's screen
            frame = wizard.frameGeometry()
            center_point = wizard.screen().availableGeometry().center()
            frame.moveCenter(center_point)
            wizard.move(frame.topLeft())
    
    
        if wizard is not None:
        #    wizard.resize(600, 500)   # or your prefer`red size
    
            frame = wizard.frameGeometry()
            center_point = wizard.screen().availableGeometry().center()
            frame.moveCenter(center_point)
            wizard.move(frame.topLeft())


    def validatePage(self) -> bool:
        acids = [cb.text() for cb in self.acid_checkboxes if cb.isChecked()]
        chiral_acids = [cb.text() for cb in self.chiral_acid_checkboxes if cb.isChecked()]
        bases = [cb.text() for cb in self.base_checkboxes if cb.isChecked()]
        chiral_bases = [cb.text() for cb in self.chiral_base_checkboxes if cb.isChecked()]
 
        self.design.selected_salt_formers = {
            "acids": acids,
            "chiral_acids": chiral_acids,
            "bases": bases,
            "chiral_bases": chiral_bases,
        }
 
        # Calculate total number of salt formers selected
        unique_salt_formers = list(set(acids + chiral_acids + bases + chiral_bases))
        self.design.no_of_salt_formers = len(unique_salt_formers)
        #     print(f"DEBUG: Number of unique salt formers selected: {self.design.no_of_salt_formers}")
 
        self.design.include_salt_free_set = bool(self.salt_free_checkbox.isVisible()
                                                     and self.salt_free_checkbox.isChecked())
 
        # Page is always valid; user may select none and move on
        return True
