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
    QScrollArea,
    QFrame,
)
from PyQt6.QtCore import Qt
from models.solvent_manager import SolventManager
from utils import normalize


class PageSolventPicker(QWizardPage):
    """
    Allows the user to select solvents from a pre-loaded database.
    Uses a two-column table layout for efficient browsing of large lists.
    """
    def __init__(self, design_model):
        super().__init__()
        self.setTitle("Select Solvents")

        # ⭐ FIXED: store the model correctly
        self.model = design_model
        self.design = design_model

        self.selected = []
        self.setTitle("Solvent Picker")

        # Load solvent list from the file path provided in the DesignModel
        self.manager = SolventManager(self.design.solvent_list_filename)
        self.manager.load()
    
        solvents = self.manager.solvents
        n = len(solvents)
    
        # Split into two columns to optimize vertical space on the screen
        half = (n + 1) // 2
        left = solvents[:half]
        right = solvents[half:]
    
        # Create a table with 4 columns: [Checkbox, Name, Checkbox, Name]
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Select", "Solvent", "Select", "Solvent"])
    
        rows = max(len(left), len(right))
        self.table.setRowCount(rows)
        for row in range(rows):
            # Populate Left Column
            if row < len(left):
                checkbox_left = QCheckBox()
                font = checkbox_left.font()
                font.setPointSize(9)
                checkbox_left.setFont(font)
                checkbox_left.setStyleSheet("font-size: 9pt;")
                widget_left = QWidget()
                hbox_left = QHBoxLayout()
                hbox_left.addWidget(checkbox_left)
                hbox_left.setAlignment(Qt.AlignmentFlag.AlignCenter)
                hbox_left.setContentsMargins(0, 0, 0, 0)
                widget_left.setLayout(hbox_left)
                self.table.setCellWidget(row, 0, widget_left)

                item_left = QTableWidgetItem(left[row]["Name"])
                # Prevent users from editing the solvent names directly in the table
                item_left.setFlags(item_left.flags() ^ Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, 1, item_left)

            # Populate Right Column
            if row < len(right):
                checkbox_right = QCheckBox()
                checkbox_right.setStyleSheet("font-size: 9pt;")
                widget_right = QWidget()
                hbox_right = QHBoxLayout()
                hbox_right.addWidget(checkbox_right)
                hbox_right.setAlignment(Qt.AlignmentFlag.AlignCenter)
                hbox_right.setContentsMargins(0, 0, 0, 0)
                widget_right.setLayout(hbox_right)
                self.table.setCellWidget(row, 2, widget_right)

                item_right = QTableWidgetItem(right[row]["Name"])
                # Prevent users from editing the solvent names directly in the table
                item_right.setFlags(item_right.flags() ^ Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, 3, item_right)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        header = self.table.horizontalHeader()
        # Set the "Select" columns (0 and 2) to a fixed width for consistency
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(0, 60)
        header.resizeSection(2, 60)
        # Set the "Solvent" columns (1 and 3) to stretch and fill available space
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
    
        for r in range(rows):
            self.table.setRowHeight(r, 28)
    
        # Styling the table to match the application's dark theme
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
    
        # Create a container widget to act as the "frame" for the table
        container_widget = QWidget()
        # Removed setFixedWidth so it can adapt to the window size
        container_layout = QVBoxLayout(container_widget)
        # Added generous margins here to create the "framed" look within the window
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.setSpacing(0)
        container_layout.addWidget(self.table)



        # Wrap the container in a scroll area to handle small screens/large lists
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setWidget(container_widget)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #3c3c3c;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #718096;
                min-height: 20px;
                border-radius: 5px;
            }
        """)

        
        # Remove the outer margin/padding from the scroll area's content to prevent double borders
        container_widget.setContentsMargins(0, 0, 0, 0)
        container_layout.setContentsMargins(10, 10, 10, 10)



        center_layout = QHBoxLayout()
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Give the container some breathing room within the center layout
        center_layout.setContentsMargins(20, 0, 20, 0)
        center_layout.addWidget(scroll_area)

        outer_layout.addLayout(center_layout)
        self.setLayout(outer_layout)
    
    def showEvent(self, event):
        """Centers the wizard window on the screen."""
        super().showEvent(event)
    
        window = self.window()
        if window is not None:
            frame = window.frameGeometry()
            center_point = window.screen().availableGeometry().center()
            frame.moveCenter(center_point)
            window.move(frame.topLeft())

    
    
    def validatePage(self) -> bool:
        """Collects all checked solvents and updates the DesignModel."""
        self.selected.clear()
    
        for row in range(self.table.rowCount()):
            # Check Left Column
            widget_left = self.table.cellWidget(row, 0)
            if widget_left:
                chk_left = widget_left.findChild(QCheckBox)
                if chk_left and chk_left.isChecked():
                    name_item = self.table.item(row, 1)
                    if name_item:
                        # Note: normalize() is used to ensure consistent naming
                        self.selected.append(normalize(name_item.text()))
    
            # Check Right Column
            widget_right = self.table.cellWidget(row, 2)
            if widget_right:
                chk_right = widget_right.findChild(QCheckBox)
                if chk_right and chk_right.isChecked():
                    name_item = self.table.item(row, 3)
                    if name_item:
                        self.selected.append(normalize(name_item.text()))
    

            # Update the model with a unique list of selected solvents
        unique_solvents = list(set(self.selected))
        no_of_solvents: int = len(unique_solvents)
        self.model.selected_solvents = unique_solvents
        self.design.selected_solvents_pca = unique_solvents
        #     print(f"DEBUG: Number of unique solvents selected: {no_of_solvents}")
        return True
