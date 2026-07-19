from PyQt6.QtWidgets import (
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QWizardPage,
    QRadioButton,
    QHBoxLayout,
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

                # --- Starting mixture options ---
        self.radio_single = QRadioButton(
            "All experiments use the same starting mixture composition"
        )
        self.radio_multiple = QRadioButton(
            "Experimental plan has several starting mixture compositions"
        )

        # Default: single mixture
        self.radio_single.setChecked(True)

        # Spin box for number of starting mixtures
        self.spin_starting = QSpinBox()
        self.spin_starting.setMinimum(2)
        self.spin_starting.setMaximum(20)
        self.spin_starting.setValue(2)
        self.spin_starting.setFixedWidth(60)
        self.spin_starting.hide()  # hidden unless multiple mixtures selected

        # Connect radio buttons
        self.radio_single.toggled.connect(self._update_starting_mix_visibility)
        self.radio_multiple.toggled.connect(self._update_starting_mix_visibility)

        # Add to layout
        layout.addSpacing(20)
        layout.addWidget(QLabel("Starting mixture options:"))
        layout.addWidget(self.radio_single)
        layout.addWidget(self.radio_multiple)

        # Horizontal layout for spin box
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Number of starting mixtures:"))
        hbox.addWidget(self.spin_starting)
        layout.addLayout(hbox)

    
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
    
    def _update_starting_mix_visibility(self):
        """Show spin box only when multiple starting mixtures are selected."""
        if self.radio_multiple.isChecked():
            self.spin_starting.show()
        else:
            self.spin_starting.hide()



    def validatePage(self) -> bool:
        """Ensures the user has selected at least one component before proceeding."""
        value = self.spin.value()
        if value < 1:
            return False

        self.design.number_of_components = value

        # Store number of starting mixtures
        if self.radio_single.isChecked():
            self.design.number_of_starting_mixtures = 1
        else:
            self.design.number_of_starting_mixtures = self.spin_starting.value()

        return True
