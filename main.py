from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
import sys
import os

from utils.paths import resource_path

def main():
    app = QApplication(sys.argv)

    # Determine the correct path to the stylesheet
    # This now correctly handles bundled files via PyInstaller's _MEIPASS
    stylesheet_path = resource_path("styles.qss")

    # Ensure the application has a consistent look across different OS
    app.setStyle("Fusion")

    # Load and apply the global style sheet
    if not os.path.exists(stylesheet_path):
        cwd_stylesheet = os.path.abspath("styles.qss")
        if os.path.exists(cwd_stylesheet):
            stylesheet_path = cwd_stylesheet

    if os.path.exists(stylesheet_path):
        with open(stylesheet_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"Warning: Stylesheet not found at {stylesheet_path}")

    from wizard.wizard_controller import DesignWizard

    wizard = DesignWizard()
    wizard.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

