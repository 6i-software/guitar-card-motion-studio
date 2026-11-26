"""Shared pytest configuration.

Forcing the offscreen Qt platform here guarantees headless test runs on CI and
on machines without a display. The variable must be set before a QApplication
is created; pytest-qt builds one from the qt_api plugin config.
"""

from __future__ import annotations

import os

os.environ["QT_QPA_PLATFORM"] = "offscreen"
