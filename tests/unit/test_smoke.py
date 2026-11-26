"""Smoke tests: package metadata and the Qt bootstrap window."""

from __future__ import annotations

from importlib import metadata

from PySide6.QtCore import QTimer
from pytestqt.qtbot import QtBot

import gcstudio
import gcstudio.core
from gcstudio.ui.app import WINDOW_TITLE, MainWindow, create_application, main


def test_package_exposes_version() -> None:
    assert gcstudio.__version__ == metadata.version("gcstudio")


def test_core_package_is_importable() -> None:
    assert gcstudio.core.__name__ == "gcstudio.core"


def test_main_window_has_expected_title(qtbot: QtBot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.windowTitle() == WINDOW_TITLE
    assert WINDOW_TITLE == "Guitar Card AI-Motion Studio"
    assert window.centralWidget() is not None


def test_main_runs_event_loop_and_exits_cleanly() -> None:
    app = create_application([])
    QTimer.singleShot(0, app.quit)
    assert main([]) == 0


def test_create_application_returns_same_instance() -> None:
    app = create_application([])
    assert create_application([]) is app
