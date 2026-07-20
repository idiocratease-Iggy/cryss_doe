from PyQt6.QtWidgets import QWizardPage, QLabel, QVBoxLayout

class PageExperimentGenerator(QWizardPage):
    def __init__(self, model):
        super().__init__()
        self.model = model

        self.setTitle("Experiment Generation")
        self.setSubTitle("Click Finish to generate your experiment sheet.")

        layout = QVBoxLayout()
        layout.addWidget(QLabel(
            "All design parameters have been collected.\n"
            "Press Finish to generate your experiment file."
        ))
        self.setLayout(layout)
