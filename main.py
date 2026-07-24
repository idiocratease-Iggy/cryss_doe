from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    app = QApplication(sys.argv)

    # Determine the correct path to the stylesheet
    # This now correctly handles bundled files via PyInstaller's _MEIPASS
    stylesheet_path = resource_path("styles.qss")

    # Load and apply the global style sheet
    if os.path.exists(stylesheet_path):
        with open(stylesheet_path, "r") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"Warning: Stylesheet not found at {stylesheet_path}")

    from wizard.wizard_controller import DesignWizard

    # Ensure the application has a consistent look across different OS
    app.setStyle("Fusion")

    wizard = DesignWizard()
    wizard.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
