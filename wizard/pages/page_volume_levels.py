from PyQt6.QtWidgets import (
    QWizardPage,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QSpinBox,
    QGroupBox,
    QRadioButton,
    QComboBox,
    QCheckBox,
)
from PyQt6.QtCore import Qt


class PageVolumeLevels(QWizardPage):
    def __init__(self, model):
        super().__init__()
        self.model = model

        self.setTitle("Solvent Volume Levels")

        # ------------------------------
        # Guidance text
        # ------------------------------
        guidance = QLabel(
            "<b>Guidance:</b><br>"
            "CRYSS experiments should be run <i>highly concentrated</i>, using low solvent volumes "
            "relative to the solid mass. This ensures that after equilibration, both phases "
            "(solid + mother liquor) contain a partially purified mixture.<br><br>"
            "If an experiment produces no solid phase, or a solid phase consisting of a pure compound, "
            "it provides no useful partitioning information for CRYSS.<br><br>"
            "Using multiple solvent volumes for the same starting composition improves solubility "
            "modelling and partitioning accuracy."
        )
        guidance.setWordWrap(True)

        # ------------------------------
        # Number of solvent volume levels
        # ------------------------------
        volumes_label = QLabel("How many solvent volume levels do you want to use?")
        self.spin_volumes = QSpinBox()
        self.spin_volumes.setMinimum(1)
        self.spin_volumes.setMaximum(10)
        self.spin_volumes.setValue(2)

        volumes_layout = QHBoxLayout()
        volumes_layout.addWidget(volumes_label)
        volumes_layout.addWidget(self.spin_volumes)

        # ------------------------------
        # Volume mode (Relative first, default)
        # ------------------------------
        mode_group = QGroupBox("Volume Mode")
        self.radio_relative = QRadioButton("Relative solvent volume (mL solvent / g mixture)")
        self.radio_absolute = QRadioButton("Absolute solvent volume")
        self.radio_relative.setChecked(True)

        mode_layout = QVBoxLayout()
        mode_layout.addWidget(self.radio_relative)
        mode_layout.addWidget(self.radio_absolute)
        mode_group.setLayout(mode_layout)

        # ------------------------------
        # Unit selector (only visible for absolute mode)
        # ------------------------------
        unit_label = QLabel("Units for absolute solvent volume:")
        self.combo_units = QComboBox()
        self.combo_units.addItems(["mL", "µL", "L", "dL", "dm³"])
        self.combo_units.setCurrentText("mL")

        unit_layout = QHBoxLayout()
        unit_layout.addWidget(unit_label)
        unit_layout.addWidget(self.combo_units)

        # Hide unit selector initially (relative mode default)
        unit_label.setVisible(False)
        self.combo_units.setVisible(False)

        # Toggle visibility when radio buttons change
        self.radio_absolute.toggled.connect(
            lambda checked: (
                unit_label.setVisible(checked),
                self.combo_units.setVisible(checked)
            )
        )

        # ------------------------------
        # Replicates section
        # ------------------------------
        replicate_group = QGroupBox("Replicates")
        self.chk_replicates = QCheckBox("Include replicates")

        replicate_label = QLabel("Replicate percentage:")
        self.spin_replicate_pct = QSpinBox()
        self.spin_replicate_pct.setRange(0, 100)
        self.spin_replicate_pct.setSuffix("%")
        self.spin_replicate_pct.setValue(0)

        replicate_layout = QHBoxLayout()
        replicate_layout.addWidget(replicate_label)
        replicate_layout.addWidget(self.spin_replicate_pct)

        replicate_box_layout = QVBoxLayout()
        replicate_box_layout.addWidget(self.chk_replicates)
        replicate_box_layout.addLayout(replicate_layout)
        replicate_group.setLayout(replicate_box_layout)

        # Hide replicate percentage until checkbox is ticked
        replicate_label.setVisible(False)
        self.spin_replicate_pct.setVisible(False)

        # Show/hide when checkbox toggled
        self.chk_replicates.toggled.connect(
            lambda checked: (
                replicate_label.setVisible(checked),
                self.spin_replicate_pct.setVisible(checked),
                self.apply_replicate_heuristic() if checked else None
            )
        )

        # ------------------------------
        # Heuristic: adjust replicate % based on number of volume levels
        # ------------------------------
        def update_replicate_default():
            if not self.chk_replicates.isChecked():
                return

            n = self.spin_volumes.value()

            if n == 1:
                default_pct = 35
            elif n == 2:
                default_pct = 25
            elif n == 3:
                default_pct = 15
            else:
                default_pct = 5

            self.spin_replicate_pct.setValue(default_pct)

        # Connect heuristic to volume-level changes
        self.spin_volumes.valueChanged.connect(update_replicate_default)

        # Also expose heuristic as a method for checkbox toggling
        self.apply_replicate_heuristic = update_replicate_default

        # ------------------------------
        # Final layout
        # ------------------------------
        layout = QVBoxLayout()
        layout.addWidget(guidance)
        layout.addSpacing(15)
        layout.addLayout(volumes_layout)
        layout.addWidget(mode_group)
        layout.addLayout(unit_layout)
        layout.addSpacing(20)
        layout.addWidget(replicate_group)
        layout.addStretch()

        self.setLayout(layout)

    # ------------------------------
    # Save data into the model
    # ------------------------------
    def validatePage(self):
        self.model.number_of_volume_levels = self.spin_volumes.value()

        if self.radio_absolute.isChecked():
            self.model.volume_mode = "absolute"
            self.model.volume_unit = self.combo_units.currentText()
        else:
            self.model.volume_mode = "relative"
            self.model.volume_unit = "mL/g"

        self.model.include_replicates = self.chk_replicates.isChecked()
        self.model.replicate_percentage = (
            self.spin_replicate_pct.value() if self.chk_replicates.isChecked() else 0
        )

        return True
