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
        self.setMinimumWidth(600)
        self.setLayout(layout)

    def _on_value_changed(self, value: int):
        self.design.number_of_starting_mixtures = value

    def validatePage(self) -> bool:
        value = self.spin.value()
        if value < 1:
            return False
        self.design.number_of_starting_mixtures = value
        return True
