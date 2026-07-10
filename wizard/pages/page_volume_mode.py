from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWizardPage


class PageVolumeMode(QWizardPage):
    def __init__(self, design_model):
        super().__init__()
        self.design = design_model


        self.setTitle("Volume Mode (placeholder)")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Volume mode not implemented yet."))
        self.setLayout(layout)

    def validatePage(self):
        return True
