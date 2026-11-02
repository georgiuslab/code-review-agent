import os
from smolagents import tool

REPO_ROOT = os.path.abspath(os.environ.get("REPO_ROOT", "."))
SKIP = {".git", "node_modules", "target", "__pycache__", ".idea"}


def _root() -> str:
    return os.path.abspath(os.environ.get("REPO_ROOT", REPO_ROOT))


def _safe(path: str) -> str:
    root = _root()
    full = os.path.abspath(os.path.join(root, path))
    if full != root and not full.startswith(root + os.sep):
        raise ValueError("Path is outside the repository")
    return full


def _entries(full: str) -> str:
    entries = sorted(e for e in os.listdir(full) if e not in SKIP)
    if not entries:
        return "Directory is empty."
    return "\n".join(
        e + "/" if os.path.isdir(os.path.join(full, e)) else e
        for e in entries
    )


def _not_found(path: str) -> str:
    return (
        f"ERROR: '{path}' does not exist in the repository. "
        f"Use only real paths. Files in the repository root:\n{_entries(_root())}"
    )


@tool
def list_files(path: str = ".") -> str:
    try:
        full = _safe(path)
        if not os.path.isdir(full):
            return _not_found(path)
        return _entries(full)
    except Exception as e:
        return f"ERROR: {e}"


@tool
def read_file(path: str, max_chars: int = 3000) -> str:
    try:
        max_chars = max_chars or 3000
        full = _safe(path)
        if not os.path.isfile(full):
            return _not_found(path)
        with open(full, encoding="utf-8") as f:
            text = f.read()
        if len(text) > max_chars:
            return text[:max_chars] + f"\n... [truncated, {len(text)} chars total]"
        return text
    except Exception as e:
        return f"ERROR: {e}"