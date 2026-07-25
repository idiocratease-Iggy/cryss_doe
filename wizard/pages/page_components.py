from PyQt6.QtWidgets import (
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QWizardPage,
    QRadioButton,
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
        self.setTitle("Define Components in Mixture, and No. Mixture Systems")
    
        layout = QVBoxLayout()
    
        label_title = QLabel("Number of components:")
        font = label_title.font()
        font.setPointSize(font.pointSize() + 2)
        font.setBold(True)
        label_title.setFont(font)
        layout.addWidget(label_title)

        label = QLabel(
            "Specify the number of chemical components in the mixture system.\n"
            "This will define how many Component columns appear in the template."
        )
    
        # Input for the number of components (Range: 1-20)
        self.spin = QSpinBox()
        self.spin.setMinimum(1)
        self.spin.setMaximum(10)  # adjust if you want more
        self.spin.setValue(3)  # sensible default
        self.spin.setFixedWidth(80)  # Fix: Set a reasonable fixed width so it doesn't stretch across the screen
        self.spin.valueChanged.connect(self._on_value_changed)
    
    
        layout.addWidget(label)
        layout.addWidget(self.spin)
        self.setMinimumWidth(600)
        
        # --- Starting mixture options ---
        self.radio_single = QRadioButton(
            "All experiments use the same starting mixture composition"
        )
        self.radio_multiple = QRadioButton(
            "Experimental plan has several starting mixture compositions"
        )
        
        font = self.radio_single.font()
        font.setPointSize(9)
        self.radio_single.setFont(font)
        self.radio_multiple.setFont(font)

        self.radio_single.setChecked(True)
        
        self.spin_starting = QSpinBox()
        self.spin_starting.setMinimum(2)
        self.spin_starting.setMaximum(10)  # adjust if you want more
        self.spin_starting.setValue(2)
        self.spin_starting.setFixedWidth(80)
        self.spin_starting.hide()
        
        self.radio_single.toggled.connect(self._update_starting_mix_visibility)
        self.radio_multiple.toggled.connect(self._update_starting_mix_visibility)
        
        layout.addSpacing(20)
        layout.addSpacing(40)
        layout.addSpacing(20)
        label_options = QLabel("Starting mixture options:")
        font = label_options.font()
        font.setPointSize(font.pointSize() + 2)
        font.setBold(True)
        label_options.setFont(font)
        layout.addWidget(label_options)
        layout.addWidget(self.radio_single)
        layout.addWidget(self.radio_multiple)
        self.label_starting_mixtures = QLabel("Number of starting mixtures:")
        self.label_starting_mixtures.hide()
        layout.addWidget(self.label_starting_mixtures)
        layout.addWidget(self.spin_starting)

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
    
    def _update_starting_mix_visibility(self):
        if self.radio_multiple.isChecked():
            self.spin_starting.show()
            self.label_starting_mixtures.show()
        else:
            self.spin_starting.hide()
            self.label_starting_mixtures.hide()




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
