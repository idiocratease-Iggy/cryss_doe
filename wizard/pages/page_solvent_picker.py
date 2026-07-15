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
from utils import normalize


class PageSolventPicker(QWizardPage):
    def __init__(self, design_model):
        super().__init__()
        self.design = design_model
        self.selected = []
        self.setTitle("Solvent Picker")
        self.setMinimumSize(600, 760)

        # Load solvent list
        self.manager = SolventManager(self.design.solvent_list_filename)
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

        rows = max(len(left), len(right))
        self.table.setRowCount(rows)

        for row in range(rows):
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

        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for r in range(rows):
            self.table.setRowHeight(r, 28)

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

    def showEvent(self, event):
        super().showEvent(event)

        window = self.window()
        if window is not None:
            window.setMinimumSize(600, 760)
            window.resize(600, 760)

            frame = window.frameGeometry()
            center_point = window.screen().availableGeometry().center()
            frame.moveCenter(center_point)
            window.move(frame.topLeft())


    def validatePage(self) -> bool:
        self.selected.clear()

        for row in range(self.table.rowCount()):
            widget_left = self.table.cellWidget(row, 0)
            if widget_left:
                chk_left = widget_left.findChild(QCheckBox)
                if chk_left and chk_left.isChecked():
                    name_item = self.table.item(row, 1)
                    if name_item:
                        self.selected.append(normalize(name_item.text()))

            widget_right = self.table.cellWidget(row, 2)
            if widget_right:
                chk_right = widget_right.findChild(QCheckBox)
                if chk_right and chk_right.isChecked():
                    name_item = self.table.item(row, 3)
                    if name_item:
                        self.selected.append(normalize(name_item.text()))

        self.design.selected_solvents_pca = list(self.selected)

        return True
