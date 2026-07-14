from PyQt6.QtWidgets import QWizard

from wizard.pages.page_components import PageComponents
from wizard.pages.page_pca import PagePCA
from wizard.pages.page_plate_format import PagePlateFormat
from wizard.pages.page_replicates import PageReplicates
from wizard.pages.page_salt_formers import PageSaltFormers
from wizard.pages.page_solvent_picker import PageSolventPicker
from models.descriptor_manager import DescriptorManager

from models.design_model import DesignModel

class DesignWizard(QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.model = DesignModel()

        # Load descriptors once
        dm = DescriptorManager(self.model.descriptor_filename)
        self.model.descriptor_df = dm.load()

        self.setWindowTitle("Mixture-centric DoE Wizard")

        # Pages
        self.page_components = PageComponents(self.model)
        self.page_solvent_picker = PageSolventPicker(self.model)
        self.page_pca = PagePCA(self.model)
        self.page_plate_format = PagePlateFormat(self.model)
        self.page_replicates = PageReplicates(self.model)
        self.page_salt_formers = PageSaltFormers(self.model)

        # Add pages in order
        self.addPage(self.page_components)
        self.addPage(self.page_solvent_picker)
        self.addPage(self.page_pca)
        self.addPage(self.page_plate_format)
        self.addPage(self.page_replicates)
        self.addPage(self.page_salt_formers)
