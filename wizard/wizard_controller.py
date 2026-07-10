from PyQt6.QtWidgets import QWizard
from wizard.pages.page_components import PageComponents
from wizard.pages.page_pca import PagePCA
from wizard.pages.page_plate_format import PagePlateFormat
from wizard.pages.page_replicates import PageReplicates
from wizard.pages.page_salt_formers import PageSaltFormers
from wizard.pages.page_solvent_picker import PageSolventPicker
from wizard.pages.page_starting_mixtures import PageStartingMixtures
from wizard.pages.page_summary import PageSummary
from wizard.pages.page_volume_levels import PageVolumeLevels
from wizard.pages.page_volume_mode import PageVolumeMode
from wizard.pages.page_pca import PagePCA
from wizard.pages.page_mixture_design import PageMixtureDesign

from models.design_model import DesignModel


class WizardController(QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.design = DesignModel()

        # Correct page order
        self.addPage(PageComponents(self.design))
        self.addPage(PageStartingMixtures(self.design))
        self.addPage(PageSolventPicker(self.design))
        self.addPage(PagePCA(self.design))          # ✔ PCA AFTER picker
        self.addPage(PageSaltFormers(self.design))
        self.addPage(PageVolumeMode(self.design))
        self.addPage(PageVolumeLevels(self.design))
        self.addPage(PageReplicates(self.design))
        self.addPage(PagePlateFormat(self.design))
        self.addPage(PageMixtureDesign(self.design))
        self.addPage(PageSummary(self.design))      # ✔ Summary LAST

        self.adjustSize()
        self.setWindowTitle("CRYSS Mixture Design Wizard")
