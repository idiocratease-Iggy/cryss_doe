from PyQt6.QtWidgets import (
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QWizardPage,
)


class PageComponents(QWizardPage):
    """
    The first step of the wizard where the user defines the scale of their experiment.
    This sets the number of chemical components, which dictates the layout 
    of the final experimental template.
    """
    def __init__(self, design_model):
        super().__init__()
        self.design = design_model
        self.setTitle("Number of Components in Mixture System")
    
        layout = QVBoxLayout()
    
        label = QLabel(
            "Specify the number of chemical components in the mixture system.\n"
            "This will define how many Component columns appear in the template."
        )
    
        # Input for the number of components (Range: 1-20)
        self.spin = QSpinBox()
        self.spin.setMinimum(1)
        self.spin.setMaximum(20)  # adjust if you want more
        self.spin.setValue(3)  # sensible default
        self.spin.setFixedWidth(60)  # Fix: Set a reasonable fixed width so it doesn't stretch across the screen
        self.spin.valueChanged.connect(self._on_value_changed)
    
    
        layout.addWidget(label)
        layout.addWidget(self.spin)
        self.setMinimumWidth(600)
        self.setLayout(layout)
        wizard = self.wizard()
    
    def showEvent(self, event):
        """
        Ensures the wizard window is centered on the screen and has a 
        consistent minimum size when first displayed.
        """
        super().showEvent(event)
    
        wizard = self.wizard()
        if wizard is not None:
            # Set standard dimensions for the wizard window
            wizard.setMinimumSize(600, 500)   # ⭐ critical
            wizard.resize(600, 500)
    
            # Center the window on the user's screen
            frame = wizard.frameGeometry()
            center_point = wizard.screen().availableGeometry().center()
            frame.moveCenter(center_point)
            wizard.move(frame.topLeft())
    
    
        if wizard is not None:
        #    wizard.resize(600, 500)   # or your prefer`red size
    
            frame = wizard.frameGeometry()
            center_point = wizard.screen().availableGeometry().center()
            frame.moveCenter(center_point)
            wizard.move(frame.topLeft())
    
    
    def _on_value_changed(self, value: int):
        """Updates the DesignModel immediately as the user interacts with the spin box."""
        self.design.number_of_components = value
    
    def validatePage(self) -> bool:
        """Ensures the user has selected at least one component before proceeding."""
        value = self.spin.value()
        if value < 1:
            return False
        self.design.number_of_components = value
        return True
