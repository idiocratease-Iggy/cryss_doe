from PyQt6.QtWidgets import (
    QWizardPage,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QRadioButton,
)
from PyQt6.QtCore import Qt, pyqtSignal

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

     #   self.scatter = pg.ScatterPlotItem()
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

        print("CLICK:", solvent)

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

        self.design_model = design_model
        self.selected = set()
        self.preselected = set(design_model.selected_solvents_pca or [])
        self.pca_df = pd.DataFrame()

        self.setTitle("Explore solvent space using PCA")

        layout = QVBoxLayout(self)

        self.label = QLabel(
            "Use the PCA plot to select or deselect solvents.\n"
            "Selected solvents will be carried forward into the mixture design."
        )
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        # --- PCA plot ---
        self.plot_widget = PCAPlotWidget(self)
        layout.addWidget(self.plot_widget)

        self.plot_widget.pointClicked.connect(self.on_point_clicked)

        # --- Y-axis selector (PC2, PC3, PC4) ---
        axis_box = QGroupBox("Y Axis")
        axis_layout = QVBoxLayout()

        self.y_buttons = []
        for i in [2, 3, 4]:
            rb = QRadioButton(f"PC{i}")
            axis_layout.addWidget(rb)
            self.y_buttons.append(rb)

        self.y_buttons[0].setChecked(True)  # PC2 default
        axis_box.setLayout(axis_layout)
        layout.addWidget(axis_box)

        for rb in self.y_buttons:
            rb.toggled.connect(self.update_axes)


    # ---------------------------------------------------------
    # Page initialization
    # ---------------------------------------------------------
    def showEvent(self, event):
            super().showEvent(event)

            window = self.window()
            if window is not None:
                # Make PCA page larger
                window.setMinimumSize(1200, 900)
                window.resize(1200, 900)

                # Optional: center window on screen
                frame = window.frameGeometry()
                center_point = window.screen().availableGeometry().center()
                frame.moveCenter(center_point)
                window.move(frame.topLeft())

    def initializePage(self):
        df = self.design_model.descriptor_df.copy()
        df["Solvent"] = df["Solvent"].apply(normalize)

        # PCA with 3 components (unchanged)
        desc_cols = [c for c in df.columns if c not in ("Solvent",)]
        X = df[desc_cols].values
        X_scaled = StandardScaler().fit_transform(X)

        pca = PCA(n_components=4)
        pcs = pca.fit_transform(X_scaled)

        self.pca_df = pd.DataFrame({
            "Solvent": df["Solvent"],
            "PC1": pcs[:, 0],
            "PC2": pcs[:, 1],
            "PC3": pcs[:, 2],
            "PC4": pcs[:, 3],
        })

        self.preselected = {normalize(s) for s in self.design_model.selected_solvents_pca}

        self.update_plot()

    def on_point_clicked(self, solvent):
        if solvent in self.preselected:
            return

        if solvent in self.selected:
            self.selected.remove(solvent)
        else:
            self.selected.add(solvent)

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
    def get_selected_solvents(self):
        return list(self.selected | self.preselected)
