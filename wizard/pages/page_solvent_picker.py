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
        self.setMinimumSize(700, 760)

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
        # Set the "Select" columns (0 and 2) to a fixed width
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(0, 60)
        header.resizeSection(2, 60)
        # Set the "Solvent" columns (1 and 3) to stretch
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        for r in range(rows):
            self.table.setRowHeight(r, 28)

        # Styling the table to look more like a contained frame
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #2b2b2b;
                border: 1px solid #444;
                gridline-color: #444;
            }
            QHeaderView::section {
                background-color: #3c3c3c;
                padding: 4px;
                border: 1px solid #444;
            }
        """)

        outer_layout = QVBoxLayout()
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Select Solvents")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer_layout.addWidget(title)

        # Create a container widget to act as the "frame"
        container_widget = QWidget()
        # Removed setFixedWidth so it can adapt to the window size
        container_layout = QVBoxLayout(container_widget)
        # Added generous margins here to create the "framed" look within the window
        container_layout.setContentsMargins(20, 10, 20, 10)
        container_layout.setSpacing(0)
        container_layout.addWidget(self.table)

        center_layout = QHBoxLayout()
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Give the container some breathing room within the center layout
        center_layout.setContentsMargins(20, 0, 20, 0)
        center_layout.addWidget(container_widget)

        outer_layout.addLayout(center_layout)
        self.setLayout(outer_layout)

    def showEvent(self, event):
        super().showEvent(event)

        window = self.window()
        if window is not None:
            window.setMinimumSize(700, 760)
            window.resize(700, 760)

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
