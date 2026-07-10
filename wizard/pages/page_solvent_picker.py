from PyQt6.QtWidgets import (
    QWizardPage,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QCheckBox,
    QWidget,
    QHBoxLayout,
    QHeaderView,
)
from PyQt6.QtCore import Qt

from models.solvent_manager import SolventManager


class PageSolventPicker(QWizardPage):
    def __init__(self, design_model):
        super().__init__()
        self.design = design_model

        self.setTitle("Solvent Picker")
        self.setMinimumSize(600, 500)

        # Load solvent list
        self.manager = SolventManager("SolventList.xlsx")
        self.manager.load()

        solvents = self.manager.solvents
        n = len(solvents)

        # Split into two columns
        half = (n + 1) // 2
        left = solvents[:half]
        right = solvents[half:]

        # Create table with 4 columns
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Select", "Solvent", "Select", "Solvent"])

        # Number of rows = longest column
        rows = max(len(left), len(right))
        self.table.setRowCount(rows)

        # Populate table
        for row in range(rows):

            # LEFT COLUMN
            if row < len(left):
                checkbox_left = QCheckBox()
                widget_left = QWidget()
                hbox_left = QHBoxLayout()
                hbox_left.addWidget(checkbox_left)
                hbox_left.setAlignment(Qt.AlignmentFlag.AlignCenter)
                hbox_left.setContentsMargins(0, 0, 0, 0)
                widget_left.setLayout(hbox_left)
                self.table.setCellWidget(row, 0, widget_left)

                item_left = QTableWidgetItem(left[row]["Name"])
                item_left.setFlags(item_left.flags() ^ Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, 1, item_left)

            # RIGHT COLUMN
            if row < len(right):
                checkbox_right = QCheckBox()
                widget_right = QWidget()
                hbox_right = QHBoxLayout()
                hbox_right.addWidget(checkbox_right)
                hbox_right.setAlignment(Qt.AlignmentFlag.AlignCenter)
                hbox_right.setContentsMargins(0, 0, 0, 0)
                widget_right.setLayout(hbox_right)
                self.table.setCellWidget(row, 2, widget_right)

                item_right = QTableWidgetItem(right[row]["Name"])
                item_right.setFlags(item_right.flags() ^ Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, 3, item_right)

        # Table appearance polish
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Row height
        for r in range(rows):
            self.table.setRowHeight(r, 28)

        # Center the table on the page
        outer_layout = QVBoxLayout()
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Select Solvents")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer_layout.addWidget(title)

        center_widget = QWidget()
        center_layout = QHBoxLayout()
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_widget.setLayout(center_layout)

        center_layout.addWidget(self.table)
        outer_layout.addWidget(center_widget)

        self.setLayout(outer_layout)

    # -----------------------------------------------------
    # Store selected solvents in design model
    # -----------------------------------------------------
    def validatePage(self):
        selected = []

        for row in range(self.table.rowCount()):
            # LEFT COLUMN
            widget_left = self.table.cellWidget(row, 0)
            if widget_left:
                checkbox_left = widget_left.layout().itemAt(0).widget()
                if checkbox_left.isChecked():
                    selected.append(self.table.item(row, 1).text().strip()) # Added .strip()

            # RIGHT COLUMN
            widget_right = self.table.cellWidget(row, 2)
            if widget_right:
                checkbox_right = widget_right.layout().itemAt(0).widget()
                if checkbox_right.isChecked():
                    selected.append(self.table.item(row, 3).text().strip()) # Added .strip()

        print("DEBUG: Picker selections =", selected)

        self.design.selected_solvents = selected
        return True
