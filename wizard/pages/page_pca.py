# MIT License
#
# Copyright (c) [2026] [Alan A. Smith]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from PyQt6.QtWidgets import (
    QWizardPage,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox,
    QRadioButton,
    QScrollArea,
    QWidget,
    QFrame,
)

from PyQt6.QtCore import Qt, pyqtSignal, QTimer

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import pyqtgraph as pg

from utils import normalize


# ---------------------------------------------------------
# PCA computation (unchanged)
# ---------------------------------------------------------
def compute_pca(df: pd.DataFrame) -> pd.DataFrame:
    numeric_df = df.drop(columns=["Solvent"], errors="ignore")
    numeric_df = numeric_df.apply(pd.to_numeric, errors="coerce")
    numeric_df = numeric_df.dropna(axis=1, how="all")
    numeric_df = numeric_df.dropna(axis=0, how="all")

    if numeric_df.shape[0] == 0:
        raise ValueError("Descriptor matrix contains no usable numeric rows for PCA.")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(numeric_df)

    pca = PCA(n_components=2)
    components = pca.fit_transform(X_scaled)

    pca_df = pd.DataFrame({
        "PC1": components[:, 0],
        "PC2": components[:, 1],
        "Solvent": df.loc[numeric_df.index, "Solvent"]
    })

    return pca_df


# ---------------------------------------------------------
# PCA Plot Widget (unchanged)
# ---------------------------------------------------------
class PCAPlotWidget(pg.PlotWidget):
    pointClicked = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.point_data = []   # ⭐ MUST exist here
        self.setBackground("k")
        self.showGrid(x=True, y=True, alpha=0.3)


        self.scatter = pg.ScatterPlotItem(symbol='o')
        self.scatter.opts['hoverable'] = True
        self.scatter.opts['hoverSize'] = 20



        self.addItem(self.scatter)
        self.scatter.sigClicked.connect(self._on_clicked)

        self.hover_label = pg.TextItem("", anchor=(0, 1))
        self.addItem(self.hover_label)
        self.hover_label.hide()

        self.scatter.sigHovered.connect(self._on_hover)


    def set_axis_labels(self, pc_y: int):
        # X axis always PC1
        self.setLabel('bottom', f"Principal Component 1")

        # Y axis depends on radio button
        self.setLabel('left', f"Principal Component {pc_y}")

    def _on_hover(self, points):
        if points is None or not hasattr(points, "__len__"):
            self.hover_label.hide()
            return

        if isinstance(points, (list, tuple)):
            p = points[0]
        else:
            p = points

        solvent = p.data() if callable(p.data) else p.data
        self.hover_label.setText(str(solvent))
        self.hover_label.setPos(p.pos())
        self.hover_label.show()

    def _on_clicked(self, plot, points):
        if points is None or len(points) == 0:
            return

        p = points[0]
        idx = p.index()   # ⭐ ALWAYS works

        solvent = self.point_data[idx]   # ⭐ MUST use this
        solvent = str(solvent)

     #   print("CLICK:", solvent)

        self.pointClicked.emit(solvent)

    def set_points(self, points):
        xs = [p["pos"][0] for p in points]
        ys = [p["pos"][1] for p in points]
        brushes = [p["brush"] for p in points]
        pens = [p["pen"] for p in points]
        sizes = [p["size"] for p in points]

        # ⭐ MUST assign solvent names here
        self.point_data = [p["data"] for p in points]

        self.scatter.setData(
            x=xs,
            y=ys,
            brush=brushes,
            pen=pens,
            size=sizes,
            data=self.point_data,   # hover uses this
            symbol='o',
            clickable=True
        )




     #   self.scatter.addPoints(spots)



# ---------------------------------------------------------
# PCA Page (with minimal Y-axis selector added)
# ---------------------------------------------------------
class PagePCA(QWizardPage):
    def __init__(self, design_model, parent=None):
        super().__init__(parent)

        # ⭐ Correct: store the model properly
        self.model = design_model
        self.design_model = design_model
        self.selected = set()
        self.preselected = set(self.model.selected_solvents or [])

        self.setTitle("PCA Solvent Selection")

        self.design_model = design_model
        self.selected = set()
        self.preselected = set(design_model.selected_solvents_pca or [])
        self.pca_model = None
        self.desc_cols = []
        self.pca_df = pd.DataFrame()

        self.setTitle("Explore solvent space using PCA")

        layout = QHBoxLayout(self)
        left_layout = QVBoxLayout()

        # Using HTML for multi-colored text
        # Orange: #FFA500, Red: #FF7878
        text = (
            "Use the PCA plot to select or deselect solvents more exotic solvents [shown in <font color='#FFA500'>Orange</font>]; "
            "good for experimental diversity.<br>"
            "Selected solvents will be carried forward into the mixture design [nb typical solvents are selected on the previous "
            "Solvent Picker dialogue are in <font color='#FF7878'>Red</font>].<br>"
            "You can adjust the plot by right click and drag to zoom, or left click and drag to pan. "
            "Hover over points to see solvent names."
        )

        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("font-size: 10px;")
        left_layout.addWidget(self.label)

        # --- PCA plot ---
        self.plot_widget = PCAPlotWidget(self)
        
        # Wrap the plot in a scroll area to handle small screens and prevent clipping
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.setSpacing(0)
        container_layout.addWidget(self.plot_widget)
        
        scroll_area.setWidget(container)
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
        
        container.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(scroll_area)


        
        layout.addLayout(left_layout)




        self.plot_widget.pointClicked.connect(self.on_point_clicked)

        # --- Y-axis selector (PC2, PC3, PC4) ---
        axis_box = QGroupBox("Y Axis")
        axis_layout = QVBoxLayout()

        self.y_buttons = []
        for i in [2, 3, 4]:
            rb = QRadioButton(f"PC{i}")
            font = rb.font()
            font.setPointSize(9)
            rb.setFont(font)
            axis_layout.addWidget(rb)
            self.y_buttons.append(rb)

        self.y_buttons[0].setChecked(True)  # PC2 default
        axis_box.setLayout(axis_layout)
        layout.addWidget(axis_box)

        for rb in self.y_buttons:
            rb.toggled.connect(self.update_axes)


        self.preselected = set(self.model.selected_solvents) # PCA page must read picker solvents from the model



    # ---------------------------------------------------------
    # Page initialization
    # ---------------------------------------------------------
    def showEvent(self, event):
        super().showEvent(event)
        # Removed hardcoded window resizing to allow other pages to control size.

    def initializePage(self):
        df = self.design_model.descriptor_df.copy()
        df["Solvent"] = df["Solvent"].apply(normalize)

        desc_cols = [c for c in df.columns if c not in ("Solvent",)]
        self.desc_cols = desc_cols
        X = df[desc_cols].values
        X_scaled = StandardScaler().fit_transform(X)
        
        self.pca_model = PCA(n_components=4)
        pcs = self.pca_model.fit_transform(X_scaled)
        
        self.pca_df = pd.DataFrame({
            "Solvent": df["Solvent"],
            "PC1": pcs[:, 0],
            "PC2": pcs[:, 1],
            "PC3": pcs[:, 2],
            "PC4": pcs[:, 3],
        })
        
        self.preselected = {normalize(s) for s in self.design_model.selected_solvents_pca}


        QTimer.singleShot(0, self.update_plot)




    def on_point_clicked(self, solvent):
        if solvent in self.preselected:
            return
 
        if solvent in self.selected:
            self.selected.remove(solvent)
        else:
            self.selected.add(solvent)
 
        # Calculate and print count for debugging
        unique_solvents = list(self.selected | self.preselected)
        self.model.selected_solvents_pca = unique_solvents
        #     print(f"DEBUG: Number of unique solvents selected in PCA: {len(unique_solvents)}")

        # Determine selected axis
        y_pc = next((i+2 for i, rb in enumerate(self.y_buttons) if rb.isChecked()), 2)
        self.update_plot(y_pc)

    # ---------------------------------------------------------
    # Axis update
    # ---------------------------------------------------------
    def update_axes(self):
        y_pc = next((i+2 for i, rb in enumerate(self.y_buttons) if rb.isChecked()), 2)

        # Update axis labels
        self.plot_widget.set_axis_labels(y_pc)

        # Update scatter positions
        self.update_plot(y_pc)


    # ---------------------------------------------------------
    # Plot update
    # ---------------------------------------------------------
    def _on_pc_selected(self, pc_y):
        # Update the PCA plot axis labels
        self.pca_plot.set_axis_labels(pc_y)

        # Recompute the scatter positions for the new PC
        self.update_pca_points(pc_y)


    def update_plot(self, y_pc=2):
        points = []
        self.plot_widget.set_axis_labels(y_pc)
        for _, row in self.pca_df.iterrows():
            solvent = row["Solvent"]

            if solvent in self.selected:
                brush = pg.mkBrush(255, 165, 0, 230)
                pen = pg.mkPen(255, 165, 0, 230)
            elif solvent in self.preselected:
                brush = pg.mkBrush(255, 120, 120, 230)
                pen = pg.mkPen(255, 120, 120, 230)
            else:
                brush = pg.mkBrush(None)
                pen = pg.mkPen(100, 150, 255, 200)

            points.append({
                "pos": (row["PC1"], row[f"PC{y_pc}"]),
                "data": solvent,
                "brush": brush,
                "pen": pen,
                "size": 12,
            })

        def sort_key(p):
            name = p["data"]
            if name in self.selected:
                return 2
            if name in self.preselected:
                return 1
            return 0

        points.sort(key=sort_key)
        self.plot_widget.set_points(points)



    # ---------------------------------------------------------
    # Final selection
    # ---------------------------------------------------------
    def export_pca_loadings(self, output_path: str):
        if self.pca_model is not None:
            save_pca_loadings(self.pca_model, self.desc_cols, output_path)
        else:
            print("PCA model not initialized.")

    def showEvent(self, event):
        super().showEvent(event)
        # Removed hardcoded window resizing to allow other pages to control size.
        # Note: The wizard's initial size is handled by the main window or previous pages.

