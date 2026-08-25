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

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor, QIcon
import sys
import os

from utils.paths import resource_path

APP_ICON_PATH = os.path.join("icons", "cryss_doe.ico")


def main():
    app = QApplication(sys.argv)

    # Determine the correct path to the stylesheet
    # This now correctly handles bundled files via PyInstaller's _MEIPASS
    stylesheet_path = resource_path("styles.qss")
    icon_path = resource_path(APP_ICON_PATH)

    # Ensure the application has a consistent look across different OS
    app.setStyle("Fusion")
    
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

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

