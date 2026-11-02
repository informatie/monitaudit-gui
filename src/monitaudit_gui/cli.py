# src/monitaudit_gui/cli.py

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    app_path = Path(__file__).with_name(
        "gui-error.py"
    )

    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(app_path),
        ],
        check=True,
    )