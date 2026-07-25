import sys
import os

def resource_path(relative_path):
    """Get absolute path to a resource, supporting both development and PyInstaller bundles."""
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # In development, styles.qss lives at the repository root
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    return os.path.join(base_path, relative_path)
