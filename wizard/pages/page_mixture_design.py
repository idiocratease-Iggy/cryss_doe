from PyQt6.QtWidgets import QWizardPage, QVBoxLayout, QLabel

class PageMixtureDesign(QWizardPage):
    def __init__(self, design_model):
        super().__init__()
        self.design = design_model

        self.setTitle("Mixture Design (placeholder)")

        layout = QVBoxLayout()
        layout.addWidget(QLabel(
            "Mixture design not implemented yet.\n"
            "This page will define the experiment matrix based on:\n"
            "- Number of components\n"
            "- Number of starting mixtures\n"
            "- Selected solvents\n"
            "- PCA selections\n"
        ))
        self.setLayout(layout)

    def validatePage(self):
        return True
