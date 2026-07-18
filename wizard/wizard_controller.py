from PyQt6.QtWidgets import QWizard

from wizard.pages.page_components import PageComponents
from wizard.pages.page_solvent_picker import PageSolventPicker
from wizard.pages.page_pca import PagePCA
from wizard.pages.page_salt_formers import PageSaltFormers
from wizard.pages.page_volume_levels import PageVolumeLevels
from wizard.pages.page_plate_picker import PagePlatePicker

from models.descriptor_manager import DescriptorManager
from models.design_model import DesignModel


class DesignWizard(QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.model = DesignModel()

        # Load descriptors once
        dm = DescriptorManager(self.model.descriptor_filename)
        self.model.descriptor_df = dm.load()

        # Load salt formers
        from models.salt_former_manager import SaltFormerManager
        sfm = SaltFormerManager(self.model.salt_former_filename)
        self.model.salt_former_data = sfm.load()

        self.setWindowTitle("Mixture-centric DoE Wizard")

        # Pages (updated)
        self.page_components = PageComponents(self.model)
        self.page_solvent_picker = PageSolventPicker(self.model)
        self.page_pca = PagePCA(self.model)
        self.page_salt_formers = PageSaltFormers(self.model)
        self.page_volume_levels = PageVolumeLevels(self.model)
        self.page_plate_picker = PagePlatePicker(self.model)

        # Add pages in order
        self.addPage(self.page_components)
        self.addPage(self.page_solvent_picker)
        self.addPage(self.page_pca)
        self.addPage(self.page_salt_formers)
        self.addPage(self.page_volume_levels)
        self.addPage(self.page_plate_picker)
