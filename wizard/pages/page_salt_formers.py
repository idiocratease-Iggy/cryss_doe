from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWizardPage


class PageSaltFormers(QWizardPage):
    def __init__(self, design_model):
        super().__init__()
        self.design = design_model


        self.setTitle("Salt Formers (placeholder)")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Salt former picker not implemented yet."))
        self.setLayout(layout)

    def validatePage(self):
        return True
