"""Guards: :mod:`gcstudio.core` must stay free of Qt and of the UI layer."""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "src"
CORE_ROOT = SRC_ROOT / "gcstudio" / "core"
FORBIDDEN_ROOTS = ("PySide6", "gcstudio.ui")

_BLOCK_QT_SCRIPT = """\
import sys


class _QtBlocker:
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "PySide6" or fullname.startswith("PySide6."):
            raise ImportError(f"PySide6 is forbidden in gcstudio.core: {fullname}")
        return None


sys.meta_path.insert(0, _QtBlocker())
import gcstudio.core

assert "PySide6" not in sys.modules
"""


def _core_modules() -> list[Path]:
    return sorted(CORE_ROOT.rglob("*.py"))


def _module_name(path: Path) -> str:
    parts = list(path.relative_to(SRC_ROOT).with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def _resolve_import(module: str | None, level: int, module_name: str) -> str:
    """Resolve a relative import against the importing module's package."""
    if level == 0:
        return module or ""
    package_parts = module_name.split(".")[:-1]
    keep = len(package_parts) - (level - 1)
    prefix = ".".join(package_parts[:keep]) if keep > 0 else ""
    if not module:
        return prefix
    return f"{prefix}.{module}" if prefix else module


def _imports(tree: ast.AST, module_name: str) -> list[tuple[str, int]]:
    found: list[tuple[str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend((alias.name, node.lineno) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = _resolve_import(node.module, node.level, module_name)
            found.append((base, node.lineno))
            found.extend(
                (f"{base}.{alias.name}" if base else alias.name, node.lineno)
                for alias in node.names
                if alias.name != "*"
            )
    return found


def _is_forbidden(imported: str) -> bool:
    return any(imported == root or imported.startswith(f"{root}.") for root in FORBIDDEN_ROOTS)


def test_core_does_not_import_qt_or_ui() -> None:
    offenders: list[str] = []
    for path in _core_modules():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for imported, lineno in _imports(tree, _module_name(path)):
            if _is_forbidden(imported):
                relative = path.relative_to(PROJECT_ROOT)
                offenders.append(f"{relative}:{lineno} imports {imported}")
    assert not offenders, "Forbidden imports in gcstudio.core:\n" + "\n".join(offenders)


def test_core_imports_without_pyside6() -> None:
    result = subprocess.run(
        [sys.executable, "-c", _BLOCK_QT_SCRIPT],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stderr
