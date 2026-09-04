"""Root conftest — ensures the project root is on sys.path so that
`from pages...` / `from utils...` imports work regardless of where
pytest is invoked from, and centralizes any shared fixtures.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
