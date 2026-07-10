from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWizardPage


class PageVolumeLevels(QWizardPage):
    def __init__(self, design_model):
        super().__init__()
        self.design = design_model


        self.setTitle("Volume Levels (placeholder)")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Volume levels not implemented yet."))
        self.setLayout(layout)

    def validatePage(self):
        return True
