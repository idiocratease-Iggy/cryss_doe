from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
import sys
import os

def main():
    app = QApplication(sys.argv)

    # Load and apply the global style sheet to improve contrast/colors
    if os.path.exists("styles.qss"):
        with open("styles.qss", "r") as f:
            app.setStyleSheet(f.read())

    from wizard.wizard_controller import DesignWizard

    # Ensure the application has a consistent look across different OS
    app.setStyle("Fusion")

    wizard = DesignWizard()
    wizard.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
