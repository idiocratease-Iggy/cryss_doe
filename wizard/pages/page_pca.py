from PyQt6.QtWidgets import (
    QWizardPage,
    QVBoxLayout,
    QLabel,
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import pyqtgraph as pg

from utils import normalize

def compute_pca(df: pd.DataFrame) -> pd.DataFrame:
    # Drop non-numeric columns except Solvent
    numeric_df = df.drop(columns=["Solvent"], errors="ignore")

    # Convert to numeric
    numeric_df = numeric_df.apply(pd.to_numeric, errors="coerce")

    # Drop columns that are entirely NaN
    numeric_df = numeric_df.dropna(axis=1, how="all")

    # Drop rows that are entirely NaN
    numeric_df = numeric_df.dropna(axis=0, how="all")

    if numeric_df.shape[0] == 0:
        raise ValueError("Descriptor matrix contains no usable numeric rows for PCA.")

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(numeric_df)

    # PCA
    pca = PCA(n_components=2)
    components = pca.fit_transform(X_scaled)

    # Build result DataFrame
    pca_df = pd.DataFrame({
        "PC1": components[:, 0],
        "PC2": components[:, 1],
        "Solvent": df.loc[numeric_df.index, "Solvent"]
    })

    #print("PCA DF shape:", self.pca_df.shape)
    #print("PCA solvents:", self.pca_df["Solvent"].tolist())

    return pca_df

class PCAPlotWidget(pg.PlotWidget):
    pointClicked = pyqtSignal(object)  # solvent name

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setBackground("k")
        self.showGrid(x=True, y=True, alpha=0.3)

        self.scatter = pg.ScatterPlotItem()


        # Enable hover support for older pyqtgraph versions
        self.scatter.opts['hoverable'] = True
        self.scatter.opts['hoverSize'] = 20   # makes hover detection easier

        self.addItem(self.scatter)

        self.scatter.sigClicked.connect(self._on_clicked)

        self.hover_label = pg.TextItem("", anchor=(0, 1))
        self.addItem(self.hover_label)
        self.hover_label.hide()



    def _on_hover(self, points):
        if points is None or len(points) == 0:
            self.hover_label.hide()
            return

        p = points[0]
        solvent = p.data()

        self.hover_label.setText(solvent)
        self.hover_label.setPos(p.pos())
        self.hover_label.show()

    def _on_clicked(self, plot, points):
        if points is None or len(points) == 0:
            return
        p = points[0]
        solvent = p.data()
        self.pointClicked.emit(solvent)

    def set_points(self, points):
        """
        points: list of dicts with keys:
        - pos: (x, y)
        - data: solvent name
        - brush
        - pen
        - size
        """
        self.scatter.setData(points)


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

        # IMPORTANT: Create plot widget here
        self.plot_widget = PCAPlotWidget(self)
        self.plot_widget.setMinimumSize(1200, 800)
        layout.addWidget(self.plot_widget)

        self.plot_widget.pointClicked.connect(self.on_point_clicked)

    def showEvent(self, event):
        super().showEvent(event)

        window = self.window()
        if window is not None:
            window.setMinimumSize(1200, 800)
            window.resize(1200, 800)

            frame = window.frameGeometry()
            center_point = window.screen().availableGeometry().center()
            frame.moveCenter(center_point)
            window.move(frame.topLeft())


    def initializePage(self):
        # Center the wizard window on screen
        wizard = self.wizard()
        if wizard is not None:
            frame = wizard.frameGeometry()
            center_point = wizard.screen().availableGeometry().center()
            frame.moveCenter(center_point)
            wizard.move(frame.topLeft())

        # Expect design_model to provide a DataFrame with descriptors and a 'Solvent' column
        df = self.design_model.descriptor_df.copy()
        self.pca_df = compute_pca(df)

        # Normalise solvent names
        df["Solvent"] = df["Solvent"].apply(normalize)

        # Standardise descriptor columns
        desc_cols = [c for c in df.columns if c not in ("Solvent",)]
        X = df[desc_cols].values
        X_scaled = StandardScaler().fit_transform(X)

        # PCA
        pca = PCA(n_components=3)
        pcs = pca.fit_transform(X_scaled)

        self.pca_df = pd.DataFrame({
            "Solvent": df["Solvent"],
            "PC1": pcs[:, 0],
            "PC2": pcs[:, 1],
            "PC3": pcs[:, 2],
        })

        # Ensure preselected set is normalised
        # #------------------------------
        # Debug Prints
        # #------------------------------
        self.preselected = {normalize(s) for s in self.design_model.selected_solvents_pca}

        #print("Selected solvents:", self.design_model.selected_solvents_pca)
        #print("Descriptor DF shape:", df.shape)
        #print("Descriptor solvents:", df["Solvent"].tolist())

        subset = df[df["Solvent"].isin(self.design_model.selected_solvents_pca)]
        #print("Subset shape:", subset.shape)
        #print("Subset solvents:", subset["Solvent"].tolist())
        # #------------------------------
        # Debug Prints
        # #------------------------------
        self.update_plot()

    def update_plot(self):
        points = []

        for _, row in self.pca_df.iterrows():
            solvent = row["Solvent"]

            if solvent in self.selected:
                # orange filled
                brush = pg.mkBrush(255, 165, 0, 230)
                pen = pg.mkPen(255, 165, 0, 230)
            elif solvent in self.preselected:
                # red filled
                brush = pg.mkBrush(255, 120, 120, 230)
                pen = pg.mkPen(255, 120, 120, 230)
            else:
                # blue hollow
                brush = pg.mkBrush(None)
                pen = pg.mkPen(100, 150, 255, 200)

            points.append({
                "pos": (row["PC1"], row["PC2"]),
                "data": solvent,
                "brush": brush,
                "pen": pen,
                "size": 12,
            })

        # Draw preselected + selected last so they sit on top
        def sort_key(p):
            name = p["data"]
            if name in self.selected:
                return 2
            if name in self.preselected:
                return 1
            return 0

        points.sort(key=sort_key)

        self.plot_widget.set_points(points)

    def on_point_clicked(self, solvent):
        # Do NOT toggle preselected solvents
        if solvent in self.preselected:
            return

        if solvent in self.selected:
            self.selected.remove(solvent)
        else:
            self.selected.add(solvent)

        self.update_plot()

    def get_selected_solvents(self):
        # Union of selected + preselected
        return list(self.selected | self.preselected)
