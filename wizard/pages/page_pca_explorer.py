from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWizardPage


class PagePCAExplorer(QWizardPage):
    def __init__(self, design_model):
        super().__init__()
        self.design = design_model


        self.setTitle("PCA Explorer (placeholder)")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("PCA explorer not implemented yet."))
        self.setLayout(layout)

    def validatePage(self):
        return True
