"""Shared pytest configuration.

Forcing the offscreen Qt platform here guarantees headless test runs on CI and
on machines without a display. It must happen before PySide6 is imported.
"""

from __future__ import annotations

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
