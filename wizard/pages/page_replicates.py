from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWizardPage


class PageReplicates(QWizardPage):
    def __init__(self, design_model):
        super().__init__()
        self.design = design_model


        self.setTitle("Replicates (placeholder)")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Replicates not implemented yet."))
        self.setLayout(layout)

    def validatePage(self):
        return True
