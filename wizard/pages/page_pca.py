from PyQt6.QtWidgets import (
    QWizardPage,
    QVBoxLayout,
    QLabel,
    QWidget,
)
from PyQt6.QtCore import Qt

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import pyqtgraph as pg
# ---------------------------------------------------------
# PCA Computation Helpers  ← FUNCTIONS GO HERE
# ---------------------------------------------------------

def load_descriptor_matrix(filename: str) -> pd.DataFrame:
    if filename.lower().endswith(".csv"):
        df = pd.read_csv(filename)
    else:
        df = pd.read_excel(filename)

    df = df.dropna()
    return df

# ---------------------------------------------------------
# PCA Plot Widget (NO preselected logic here)
# ---------------------------------------------------------
class PCAPlotWidget(QWidget):
    def __init__(self, pca_df):
        super().__init__()

        self.pca_df = pca_df
        self.selected = set()
        self.preselected = set()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.plot = pg.PlotWidget()
        self.plot.setLabel('bottom', 'PC1')
        self.plot.setLabel('left', 'PC2')
        self.plot.showGrid(x=True, y=True, alpha=0.3)

        layout.addWidget(self.plot)
        self.setLayout(layout)

        self.scatter = pg.ScatterPlotItem()
        self.plot.addItem(self.scatter)

        self.scatter.sigClicked.connect(self.on_point_clicked)

        self.update_plot()

    def update_plot(self):
        points = []
        for _, row in self.pca_df.iterrows():
            solvent = row['Solvent']

            brush = (
                pg.mkBrush(255, 120, 120, 230) if solvent in self.preselected
                else pg.mkBrush(100, 150, 255, 200)
            )

            points.append({
                'pos': (row['PC1'], row['PC2']),
                'data': solvent,
                'brush': brush,
                'size': 10,
            })

        self.scatter.setData(points)

    def on_point_clicked(self, plot, points):
        p = points[0]
        solvent = p.data()

        # Do NOT toggle preselected solvents
        if solvent in self.preselected:
            return

        # Normal toggle for non-preselected solvents
        if solvent in self.selected:
            self.selected.remove(solvent)
        else:
            self.selected.add(solvent)


        # recolour
        for sp in self.scatter.points():
            name = sp.data()
            if name in self.selected:
                sp.setBrush(pg.mkBrush(255, 165, 0, 230))  # orange
            elif name in self.preselected:
                sp.setBrush(pg.mkBrush(255, 120, 120, 230))  # red
            else:
                sp.setBrush(pg.mkBrush(100, 150, 255, 200))  # blue

    def get_selected_solvents(self):
        return list(self.selected | self.preselected)


# ---------------------------------------------------------
# PCA Computation Helpers
# ---------------------------------------------------------
def load_descriptor_matrix(filename: str) -> pd.DataFrame:
    df = pd.read_excel(filename)
    df = df.dropna()
    return df


def compute_pca(df: pd.DataFrame) -> pd.DataFrame:
    solvents = df['Solvent']

    X = df.drop(columns=['Solvent', 'Code'])
    X = X.apply(pd.to_numeric, errors='coerce')

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=3)
    pcs = pca.fit_transform(X_scaled)

    return pd.DataFrame({
        'Solvent': solvents,
        'PC1': pcs[:, 0],
        'PC2': pcs[:, 1],
        'PC3': pcs[:, 2],
    })


# ---------------------------------------------------------
# PCA Wizard Page (THIS is where preselected logic lives)
# ---------------------------------------------------------
class PagePCA(QWizardPage):
    def __init__(self, design_model):
        super().__init__()

        self.design = design_model
        self.preselected = set()

        self.setTitle("PCA Explorer")
        self.setMinimumSize(600, 500)

        layout = QVBoxLayout()

        help_label = QLabel(
            "Explore the solvent descriptor space using PCA.\n"
            "Click points in the plot to select or deselect solvents.\n"
            "Selections here will be carried forward into the mixture design."
        )
        help_label.setWordWrap(True)
        layout.addWidget(help_label)

        # ⭐ Correct filename
        df = load_descriptor_matrix("Descriptors.xlsx")

        self.pca_df = compute_pca(df)

        self.plot_widget = PCAPlotWidget(self.pca_df)
        layout.addWidget(self.plot_widget)

        self.setLayout(layout)

    def initializePage(self):
        self.preselected = set(self.design.selected_solvents)
        print("DDEBUG: initializePage preselected =", self.preselected)

        self.plot_widget.preselected = self.preselected
        self.plot_widget.selected = set()
        self.plot_widget.update_plot()

    def validatePage(self):
        final = self.plot_widget.get_selected_solvents()
        self.design.selected_solvents = final

        print("DDEBUG: Final Pick-List Selection =", final)
        return True

    # -----------------------------------------------------
    # PagePCA decides colours (NOT the widget)
    # -----------------------------------------------------
    # -----------------------------------------------------
    # PagePCA decides colours (NOT the widget)
    # -----------------------------------------------------





        # If points are passed directly, use them. Otherwise, let the
        # widget handle the logic based on its internal pre_selection state.
        # This ensures that both current selections and pre-selections
        # remain visible after interaction.
        #self.plot_widget.update_plot()


    # -----------------------------------------------------
    # Merge PCA selections with picker selections
    # -----------------------------------------------------
    def initializePage(self):
        # Now the picker has run, so selected_solvents is populated
        self.preselected = set(self.design.selected_solvents)
        print("DDEBUG: initializePage preselected =", self.preselected)

        # Sync the pre-selection with the widget's internal state
        self.plot_widget.preselected = self.preselected
        self.plot_widget.selected = set()   # ← EMPTY, not preselected
        self.plot_widget.update_plot()


        # --- START OF DEBUG BLOCK ---
        problematic = ['1-butanol', '1-propanol', '1,4-dioxane']
        for p in problematic:
            if p not in self.preselected:
                print(f"DDEBUG: {p} NOT found in preselected set.")
                # Check for whitespace or case issues specifically
                found_match = False
                for item in self.preselected:
                    if p.strip() == str(item).strip():
                        print(f"DDEBUG: Found match for {p} as '{item}'")
                        found_match = True
                        break
                if not found_match:
                    # Check against the raw PCA data to see if it exists there at all
                    found_in_df = False
                    for df_val in self.pca_df['Solvent']:
                        if p.strip() == str(df_val).strip():
                            print(f"DDEBUG: {p} found in PCA DataFrame as '{df_val}'")
                            found_in_df = True
                            break
                    if not found_in_df:
                        print(f"DDEBUG: {p} NOT FOUND IN ANY LISTS.")
            else:
                print(f"DDEBUG: {p} is present in preselected.")
        # --- END OF DEBUG BLOCK ---

        # Recolour PCA points
        self.plot_widget.update_plot()

    def validatePage(self):
        # Get all currently active solvents from the widget (both Red and Orange).
        current_selection = self.plot_widget.get_selected_solvents()

        # Update the design model with the final list of selected items.
        self.design.selected_solvents = list(current_selection)

        # Calculate which ones were added specifically on this page (the Orange ones).
        newly_selected = [s for s in current_selection if s not in self.preselected]

        # Debug outputs:
        print("DDEBUG: Newly selected on PCA (Orange):", newly_selected)
        print("DDEBUG: Final Pick-List Selection =", self.design.selected_solvents)

        return True
