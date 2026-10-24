import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

if __package__:
    from .appearance import apply_system_theme
    from .window import CANViewerFullWindow
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from can_analyser.appearance import apply_system_theme
    from can_analyser.window import CANViewerFullWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_system_theme(app)
    viewer = CANViewerFullWindow()
    viewer.show()
    sys.exit(app.exec())