from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWizardPage


class PagePlateFormat(QWizardPage):
    def __init__(self, design_model):
        super().__init__()
        self.design = design_model


        self.setTitle("Plate Format (placeholder)")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Plate format not implemented yet."))
        self.setLayout(layout)

    def validatePage(self):
        return True
