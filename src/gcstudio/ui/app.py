"""Qt bootstrap for Guitar Card AI-Motion Studio."""

from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

WINDOW_TITLE = "Guitar Card AI-Motion Studio"
PLACEHOLDER_TEXT = "Fenêtre de démarrage — scaffold M0 (T-0001)"


class MainWindow(QMainWindow):
    """Minimal placeholder window, replaced by the real workspace in M1."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(960, 540)
        label = QLabel(PLACEHOLDER_TEXT)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)


def create_application(argv: list[str] | None = None) -> QApplication:
    """Return the current ``QApplication`` or create one.

    Keeping the instance out of a module-level global lets tests build and tear
    down the application explicitly.
    """
    existing = QApplication.instance()
    if isinstance(existing, QApplication):
        return existing
    return QApplication(sys.argv if argv is None else argv)


def main(argv: list[str] | None = None) -> int:
    """Run the Qt event loop and return the process exit code."""
    app = create_application(argv)
    window = MainWindow()
    window.show()
    return int(app.exec())
