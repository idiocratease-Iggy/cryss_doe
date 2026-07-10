from PyQt6.QtWidgets import (
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QWizardPage,
)


class PageComponents(QWizardPage):
    def __init__(self, design_model):
        super().__init__()
        self.design = design_model
        self.setTitle("Number of Components in Mixture System")

        layout = QVBoxLayout()

        label = QLabel(
            "Specify the number of chemical components in the mixture system.\n"
            "This will define how many Component columns appear in the template."
        )

        self.spin = QSpinBox()
        self.spin.setMinimum(1)
        self.spin.setMaximum(20)  # adjust if you want more
        self.spin.setValue(3)  # sensible default
        self.spin.valueChanged.connect(self._on_value_changed)
        

        layout.addWidget(label)
        layout.addWidget(self.spin)
        self.setMinimumWidth(600)
        self.setLayout(layout)

    def _on_value_changed(self, value: int):
        # live update if you want; final write happens in validatePage
        self.design.number_of_components = value

    def validatePage(self) -> bool:
        value = self.spin.value()
        if value < 1:
            return False
        self.design.number_of_components = value
        return True
