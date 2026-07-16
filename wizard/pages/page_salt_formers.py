from PyQt6.QtWidgets import (
    QWizardPage,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox,
    QCheckBox,
)
from PyQt6.QtCore import Qt


class PageSaltFormers(QWizardPage):
    def __init__(self, design_model):
        super().__init__()
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

        main_layout.addLayout(columns_layout)

        # 5. Salt-free checkbox (hidden until needed)
        self.salt_free_checkbox = QCheckBox("Include a salt-free control set")
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
        wizard = self.wizard()
        if wizard is not None:
            wizard.setMinimumSize(900, 850)
            wizard.resize(900, 850)

        # Call the helper method you already wrote!
        self.update_salt_free_visibility()


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

        self.design.include_salt_free_set = bool(self.salt_free_checkbox.isVisible()
                                                    and self.salt_free_checkbox.isChecked())

        # Page is always valid; user may select none and move on
        return True
