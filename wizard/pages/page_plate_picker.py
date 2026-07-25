from PyQt6.QtWidgets import (
    QWizardPage,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox,
    QRadioButton,
    QSpinBox,
    QCheckBox,
    QWidget,
    QPushButton,
    QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPainter, QPen, QFont
from PyQt6.QtWidgets import QSizePolicy

import string

from excel_writer import save_experiments_to_excel
from experiment_generator import generate_experiments

# ---------------------------------------------------------
# Plate Preview Widget
# ---------------------------------------------------------
class PlatePreview(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rows = 0
        self.cols = 0
        self.setMinimumSize(600, 600)

    def set_plate(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.update()

    def paintEvent(self, event):
        if self.rows <= 0 or self.cols <= 0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # White lines/text for dark theme
        pen_plate = QPen(Qt.GlobalColor.white, 2)
        pen_well = QPen(Qt.GlobalColor.white, 1)
        painter.setPen(pen_plate)
        painter.setFont(QFont("Arial", 12))

        # --- Compute available area ---
        margin = 40
        avail_w = self.width() - 2 * margin
        avail_h = self.height() - 2 * margin

        # --- Logical plate size (unscaled) ---
        logical_w = self.cols
        logical_h = self.rows

        # --- Compute scale factor ---
        scale_x = avail_w / logical_w
        scale_y = avail_h / logical_h
        scale = min(scale_x, scale_y) * 0.65

        # --- Compute actual plate size after scaling ---
        plate_w = logical_w * scale
        plate_h = logical_h * scale

        # --- Center the plate ---
        #plate_x = (self.width() - plate_w) / 2
        #plate_y = (self.height() - plate_h) / 2
        plate_x = 40   # left margin
        plate_y = 40   # top margin

        # --- Draw plate outline ---
        painter.drawRect(int(plate_x), int(plate_y), int(plate_w), int(plate_h))

        # --- Well spacing ---
        well_spacing_x = scale
        well_spacing_y = scale
        well_diameter = scale * 0.6

        # --- Draw wells ---
        painter.setPen(pen_well)

        for r in range(self.rows):
            for c in range(self.cols):
                cx = plate_x + c * well_spacing_x + well_spacing_x / 2
                cy = plate_y + r * well_spacing_y + well_spacing_y / 2

                painter.drawEllipse(
                    int(cx - well_diameter / 2),
                    int(cy - well_diameter / 2),
                    int(well_diameter),
                    int(well_diameter)
                )

        # --- Row labels (A, B, C…) ---
        for r in range(self.rows):
            label = string.ascii_uppercase[r]
            y = plate_y + r * well_spacing_y + well_spacing_y / 2 + 5
            painter.drawText(int(plate_x - 30), int(y), label)

        # --- Column labels (1, 2, 3…) ---
        for c in range(self.cols):
            label = str(c + 1)
            x = plate_x + c * well_spacing_x + well_spacing_x / 2 - 5
            painter.drawText(int(x), int(plate_y - 10), label)


# ---------------------------------------------------------
# Plate Picker Page
# ---------------------------------------------------------
class PagePlatePicker(QWizardPage):
    def __init__(self, model):
        super().__init__()
        self.setTitle("Select Plate Format")

        self.model = model

        self.setTitle("Select Plate Format")


        # ⭐ Create main layout FIRST
        main_layout = QHBoxLayout(self)

        # -----------------------------------------------------
        # LEFT SIDE — Format selection + randomization
        # -----------------------------------------------------
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)


        # ⭐ Now create the radio buttons
        format_group = QGroupBox("Plate Format")
        format_layout = QVBoxLayout()

        self.rb_4x3 = QRadioButton("4 × 3 (12 wells)")
        self.rb_3x5 = QRadioButton("3 × 5 (15 wells)")
        self.rb_6x4 = QRadioButton("6 × 4 (24 wells)")
        self.rb_8x6 = QRadioButton("8 × 6 (48 wells)")
        self.rb_12x8 = QRadioButton("12 × 8 (96 wells)")
        self.rb_free = QRadioButton("Free format:")
        
        # Apply smaller font to radio buttons to prevent cropping
        for rb in [self.rb_4x3, self.rb_3x5, self.rb_6x4, self.rb_8x6, self.rb_12x8, self.rb_free]:
            font = rb.font()
            font.setPointSize(9)
            rb.setFont(font)
            rb.setStyleSheet("font-size: 9pt;")
            
        self.spin_cols = QSpinBox()
        self.spin_rows = QSpinBox()
        self.spin_rows.setRange(1, 26)
        self.spin_cols.setRange(1, 50)
        self.spin_rows.setEnabled(False)
        self.spin_cols.setEnabled(False)

        free_layout = QHBoxLayout()
        free_layout.addWidget(QLabel("Rows:"))
        free_layout.addWidget(self.spin_rows)
        free_layout.addWidget(QLabel("Cols:"))
        free_layout.addWidget(self.spin_cols)

        format_layout.addWidget(self.rb_4x3)
        format_layout.addWidget(self.rb_3x5)
        format_layout.addWidget(self.rb_6x4)
        format_layout.addWidget(self.rb_8x6)
        format_layout.addWidget(self.rb_12x8)
        format_layout.addWidget(self.rb_free)
        format_layout.addLayout(free_layout)

        format_group.setLayout(format_layout)
        left_layout.addWidget(format_group)

        # Randomization option
        self.chk_randomize = QCheckBox("Randomize experiment order across reactors")
        left_layout.addWidget(self.chk_randomize)

        # Randomization explanation (now visible)
        guidance = QLabel(
            "If you suspect uneven heating or stirring across the array, enable randomization "
            "to distribute experiments across wells."
        )
        guidance.setWordWrap(True)
        guidance.setStyleSheet("color: #CCCCCC;")
        left_layout.addWidget(guidance)

        # Fill-to-full-plates option
        self.checkbox_fill_full = QCheckBox("Fill up to full plates")
        left_layout.addWidget(self.checkbox_fill_full)

        # Write Excel Button (Moved up for visibility)
        self.btn_write = QPushButton("Write Excel File")
        self.btn_write.clicked.connect(self.write_excel)
        # Assign an object name so we can style it specifically in styles.qss if needed
        self.btn_write.setObjectName("write_excel_btn")
        left_layout.addWidget(self.btn_write)

        left_layout.addStretch()

        # -----------------------------------------------------
        # RIGHT SIDE — Plate preview
        # -----------------------------------------------------
        self.preview = PlatePreview()
        self.preview.setMinimumSize(600, 600)
        self.preview.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_layout.addWidget(self.preview)

        # -----------------------------------------------------
        # SIGNALS
        # -----------------------------------------------------
        self.rb_4x3.toggled.connect(lambda: self.update_preview(3, 4))
        self.rb_3x5.toggled.connect(lambda: self.update_preview(3, 5))
        self.rb_6x4.toggled.connect(lambda: self.update_preview(4, 6))
        self.rb_8x6.toggled.connect(lambda: self.update_preview(6, 8))
        self.rb_12x8.toggled.connect(lambda: self.update_preview(8, 12))

        self.rb_free.toggled.connect(self.enable_free_format)
        self.spin_rows.valueChanged.connect(self.update_free_preview)
        self.spin_cols.valueChanged.connect(self.update_free_preview)

        # Default selection
        self.rb_6x4.setChecked(True)
        self.update_preview(4, 6)


    # ---------------------------------------------------------
    # Preview update logic
    # ---------------------------------------------------------
    def enable_free_format(self):
        free = self.rb_free.isChecked()
        self.spin_rows.setEnabled(free)
        self.spin_cols.setEnabled(free)
        if free:
            self.update_free_preview()

    def update_free_preview(self):
        if self.rb_free.isChecked():
            self.preview.set_plate(self.spin_rows.value(), self.spin_cols.value())

    def update_preview(self, rows, cols):
        sender = self.sender()
        if sender is None or sender.isChecked():
            self.preview.set_plate(rows, cols)

    def showEvent(self, event):
        super().showEvent(event)
        wizard = self.wizard()
        if wizard is not None:
            # Removed hardcoded resize to allow for dynamic scaling on different resolutions
             # Set standard dimensions for the wizard window
            wizard.setMinimumSize(600, 500)   # ⭐ critical
            wizard.resize(750, 550)
            
           # pass

        # Force correct initial preview AFTER window is sized
        if self.rb_4x3.isChecked():
            self.update_preview(3, 4)
        elif self.rb_3x5.isChecked():
            self.update_preview(3, 5)
        elif self.rb_6x4.isChecked():
            self.update_preview(4, 6)
        elif self.rb_8x6.isChecked():
            self.update_preview(6, 8)
        elif self.rb_12x8.isChecked():
            self.update_preview(8, 12)


    # ---------------------------------------------------------
    # Save results into DesignModel
    # ---------------------------------------------------------
    def write_excel(self):
        # 1. Update model with current UI selections
        self.validatePage()
        
        # 2. Generate experiments
        experiments = generate_experiments(self.model)
        
        # 3. Write Excel file
        success = save_experiments_to_excel(
            parent=self,
            experiments=experiments,
            num_components=self.model.number_of_components,
            volume_mode=self.model.volume_mode,
            volume_unit=self.model.volume_unit
        )
        
        # 4. Notify user
        if success:
            QMessageBox.information(
                self,
                "Excel Written",
                "The CRYSS experiment template has been written successfully."
            )
        else:
            QMessageBox.warning(
                self,
                "Save Failed",
                "The Excel file could not be saved. Please ensure the file is not open in another program and try again."
            )

    # ---------------------------------------------------------
    # Save results into DesignModel
    # ---------------------------------------------------------
    def validatePage(self):
        if self.rb_4x3.isChecked():
            rows, cols = 4, 3
            free = False
        elif self.rb_3x5.isChecked():
            rows, cols = 3, 5
            free = False
        elif self.rb_6x4.isChecked():
            rows, cols = 4, 6
            free = False
        elif self.rb_8x6.isChecked():
            rows, cols = 6, 8
            free = False
        elif self.rb_12x8.isChecked():
            rows, cols = 8, 12
            free = False
        else:
            rows = self.spin_rows.value()
            cols = self.spin_cols.value()
            free = True

        self.model.plate_rows = rows
        self.model.plate_cols = cols
        self.model.free_format = free
        self.model.randomize_design = self.chk_randomize.isChecked()
        self.model.fill_to_full_plates = self.checkbox_fill_full.isChecked()

        return True
